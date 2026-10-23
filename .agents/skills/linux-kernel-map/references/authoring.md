# Authoring

Generate a buildable, hardware-capable module or driver scaffold. Datasheet-level register semantics,
timing, and firmware contracts are out of scope; the kernel-side scaffold and callback contracts are
verified.

## Scaffold classes

| Class      | Use when                                        | Key APIs                                                                        |
| ---------- | ----------------------------------------------- | ------------------------------------------------------------------------------- |
| `char`     | Character device with a `file_operations` table | `alloc_chrdev_region`, `cdev_init`, `cdev_add`, `class_create`, `device_create` |
| `misc`     | Small device using the misc device framework    | `misc_register`, `misc_deregister`                                              |
| `platform` | Device described in device tree or ACPI         | `platform_driver_register`, `platform_get_irq`, `devm_ioremap_resource`         |
| `pci`      | PCI device                                      | `pci_register_driver`, `pci_enable_device`, `pci_request_regions`               |
| `usb`      | USB device                                      | `usb_register`, `usb_deregister`                                                |

## Registration order (character device)

1. `alloc_chrdev_region` — reserve a major/minor range.
2. `cdev_init` — bind the `file_operations` table.
3. `cdev_add` — make the device live.
4. `class_create` — create the device class.
5. `device_create` — create the `/dev` node.

Teardown is the exact reverse, with error unwinding at every step: if step `n` fails, undo steps
`n-1 .. 1` in reverse.

## file_operations contract

```c
static const struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = dev_open,
    .release = dev_release,
    .read = dev_read,
    .write = dev_write,
    .unlocked_ioctl = dev_ioctl,
};
```

State which callbacks may sleep (`read`, `write`, `ioctl`, `open`, `release`) and which must not
(interrupt handlers, softirq context).

## Bus driver (platform) skeleton

1. Define `struct platform_driver` with `.probe`, `.remove`, `.driver.name`, and `.driver.of_match_table`.
2. In `probe`: get resources (`platform_get_resource`, `platform_get_irq`), map registers
   (`devm_ioremap_resource`), request the interrupt, allocate DMA buffers, register child devices,
   and enable runtime PM.
3. In `remove`: disable runtime PM, free the interrupt, unmap, and unregister in reverse order.
4. Use `module_platform_driver()` to wire `module_init`/`module_exit`.

## Interrupt handling

- Request with `request_irq` or `devm_request_irq`; free with `free_irq` in teardown order.
- Hardirq handlers must not sleep; use threaded IRQs (`request_threaded_irq`) when work is heavy.
- Disable the interrupt source before freeing it; free before unmapping registers.

## DMA

- Map with `dma_map_single` / `dma_map_sg` and unmap with the matching `dma_unmap_*` call.
- State the direction (`DMA_TO_DEVICE`, `DMA_FROM_DEVICE`, `DMA_BIDIRECTIONAL`) explicitly; never
  leave it implicit.
- On non-coherent architectures, clean or invalidate the cache around the mapping and add the
  required memory barriers. Never assume cache coherency.
- Free coherent allocations with `dma_free_coherent`.

## Power management

Provide `dev_pm_ops` with at least:

- `.suspend` / `.resume` (or `.freeze`/`.thaw` for hibernation), and
- `.runtime_suspend` / `.runtime_resume` / `.runtime_idle` for runtime PM.

Order: suspend devices before their parents; resume parents before children.

## Locking and lifetime

- State which lock protects which field.
- State who owns each allocation and when it is freed.
- A device must not be freed while an interrupt or DMA transfer can still reference it.

## Build verification

```bash
make -C "$KERNEL_SRC" M="$PWD" modules
```

Expected: the module compiles and links with no errors; `modinfo` shows the license and
description.

## Out of scope

Register semantics, timing diagrams, firmware contracts, and certification sign-off are out of
scope. The kernel-side scaffold, callback contracts, and build verification remain verified.

## Answer shape (authoring)

- `Driver class:`, `Files:`, `Config gate:`, `Registration order:`, `Teardown order:`,
  `Callbacks:` (name, signature, sleeps), `IRQ:`, `DMA:`, `Power management:`,
  `Locking and lifetime:`, `Build verification:`, `Out of scope:`.
- Every API named must resolve in the pinned tree; if the scaffold was not built, `Status` is
  `partial`.
