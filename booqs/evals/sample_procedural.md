# Server Hardening: A Step-by-Step Guide

## Introduction

This guide walks through the process of hardening a Linux server for production use. Follow each step in order.

## Prerequisites

- A Linux server with SSH access (Ubuntu 22.04+ or RHEL 9+)
- Root or sudo privileges
- An internet connection

## Step 1: Update the System

First, update all system packages to the latest versions. This ensures you have the latest security patches.

On Ubuntu/Debian:

```bash
sudo apt update && sudo apt upgrade -y
```

On RHEL/Fedora:

```bash
sudo dnf upgrade --refresh -y
```

### Step 1.1: Enable Automatic Security Updates

Configure unattended upgrades to apply security patches automatically.

On Ubuntu, install and configure unattended-upgrades:

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

On RHEL, use dnf-automatic:

```bash
sudo dnf install dnf-automatic -y
sudo systemctl enable --now dnf-automatic.timer
```

## Step 2: Create a Non-Root User

Creating a non-root user for daily operations limits the blast radius of any compromise.

```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
```

## Step 3: Configure SSH Hardening

SSH is the primary attack surface. Secure it by editing `/etc/ssh/sshd_config`.

```bash
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
```

Restart SSH to apply changes:

```bash
sudo systemctl restart sshd
```

**Important:** Before closing your current SSH session, open a second terminal and verify you can connect on port 2222 with key-based authentication. Locking yourself out is a common mistake.

## Step 4: Set Up Firewall (UFW)

Configure UFW to allow only necessary traffic:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp comment 'SSH on custom port'
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'
sudo ufw --force enable
```

Verify with `sudo ufw status verbose`.

## Step 5: Install and Configure Fail2ban

Fail2ban protects against brute-force attacks by temporarily banning IPs with too many failed login attempts.

```bash
sudo apt install fail2ban -y
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

Edit `/etc/fail2ban/jail.local` and set:

```
[sshd]
enabled = true
port = 2222
maxretry = 3
bantime = 3600
```

Then start the service:

```bash
sudo systemctl enable --now fail2ban
```

## Step 6: Harden Kernel Parameters

Edit `/etc/sysctl.conf` to add these security settings:

```
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
# Disable ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
# Disable source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
```

Apply with `sudo sysctl -p`.

## Step 7: Set Up Log Monitoring with Auditd

Install and configure auditd to track security-relevant events:

```bash
sudo apt install auditd -y
```

Add rules in `/etc/audit/rules.d/audit.rules`:

```
-w /etc/ssh/sshd_config -p wa -k ssh_config
-w /etc/passwd -p wa -k user_db
-w /etc/shadow -p wa -k user_db
-a exit,always -F arch=b64 -S execve -k process_execution
```

Enable and start:

```bash
sudo systemctl enable --now auditd
```

## Step 8: Run a Security Audit

Finally, run Lynis to verify your hardening:

```bash
sudo apt install lynis -y
sudo lynis audit system
```

Review the report. Address any warnings marked with a `[W]`.

## Summary

| Step | Action                 | Tool/Command   | Verification                             |
| ---- | ---------------------- | -------------- | ---------------------------------------- |
| 1    | Update packages        | apt/dnf        | `apt list --upgradable` shows nothing    |
| 2    | Create user            | `adduser`      | `id deploy` returns user info            |
| 3    | Lock SSH               | sed, systemctl | SSH on port 2222, key-only               |
| 4    | Firewall               | ufw            | `ufw status verbose` shows rules         |
| 5    | Brute force protection | fail2ban       | `fail2ban-client status sshd`            |
| 6    | Kernel hardening       | sysctl         | `sysctl net.ipv4.conf.all.rp_filter` = 1 |
| 7    | Audit                  | auditd         | `auditctl -l` lists rules                |
| 8    | Audit                  | lynis          | Report has no [W] warnings               |

## Troubleshooting

### SSH Connection Refused

If you can't connect after changing the SSH port, check:

1. UFW is allowing port 2222
2. SSHD is running: `sudo systemctl status sshd`
3. The port change was applied: `sudo ss -tlnp | grep 2222`

### Firewall Locked You Out

If ufw blocks your connection, use the out-of-band console (iDRAC, IPMI, or hosting provider's web console) to log in and run `sudo ufw disable`.
