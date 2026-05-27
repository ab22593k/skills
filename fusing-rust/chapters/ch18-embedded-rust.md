# Embedded Rust

## Core concepts

- **Embedded systems** are specialized computing devices performing dedicated functions (Arduino, Raspberry Pi Pico)
- **Microcontroller architecture**: Harvard (separate program/data memory) vs Von Neumann (unified memory)
- **HAL (Hardware Abstraction Layer)** provides a portable interface to microcontroller peripherals — abstracts GPIO, timers, UART, SPI, I2C, ADC
- **AVR-Rust toolchain**: Rust compiler + LLVM AVR backend + AVR-Libc + `avr-device` crate
- **Flashing**: `cargo objcopy` converts ELF to binary, `avrdude` writes to Arduino Uno
- Peripherals: Timers/Counters, UART (serial), SPI/I2C (sensor communication), ADC (analog reading)

## Frameworks introduced

**HAL pattern** — Separates hardware-specific register manipulation (unsafe, platform-dependent) from application logic (safe, portable). Without HAL: `unsafe { *gpio_register ^= 1 << 5; }`. With HAL: `hal.toggle_gpio_pin(5);`.

## Key techniques

- LED blink on Arduino Uno:
  ```rust
  use arduino_uno::prelude::*;
  let mut peripherals = arduino_uno::Peripherals::take().unwrap();
  let mut pins = peripherals.pins;
  let mut led = pins.d13.into_output();
  loop {
      led.toggle();
      arduino_uno::delay_ms(1000);
  }
  ```
- ADC reading: `let adc = Adc::new(dp.ADC); adc.read(&mut dp.PORTC, adc::channel::Adc0);`
- Target spec: create `.json` file with `cpu: "atmega328p"`, `llvm-target: "avr-unknown-unknown"`

## Code examples

```rust
// Arduino Uno LED blink (simplified)
#![no_std]
#![no_main]

use arduino_uno::prelude::*;

#[arduino_uno::entry]
fn main() -> ! {
    let dp = arduino_uno::Peripherals::take().unwrap();
    let mut pins = dp.pins;
    let mut led = pins.d13.into_output();
    loop {
        led.toggle();
        arduino_uno::delay_ms(1000);
    }
}
```

## Connection to other chapters

Embedded Rust uses `unsafe` (Ch16) for register manipulation. The HAL pattern is similar to FFI (Ch17) — abstracting a lower-level interface. `#![no_std]` connects to Rust's bare-metal capabilities.
