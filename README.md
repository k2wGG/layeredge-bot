# layeredge-auto
Autofarm layeredge node testnet

![photo_2025-02-16_21-21-21](https://github.com/user-attachments/assets/8e1be1e6-01e7-43a2-aec4-055cf8b704ce)


Quick start

1. past private keys in `configs/register.txt`
2. past proxies in `configs/proxies.txt` in format `http://login:password@ip:port`
3. past ref codes in `configs/REFS.txt`
4. run `INSTALL.txt`
5. run `START.txt`

After the account is registered, it immediately starts farming, you do not need to restart the soft to start farming, but if you stop it, you need to move the private keys from `results/success.txt` to `configs/farm.txt` and in the `configs/config`: `FARM_MODE = True`
