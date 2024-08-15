# Lines to add to ```.bashrc```

These are the lines that you should add to your ```.bashrc``` file during the installation process. Be careful to ensure the version numbers are correct for your installation.

```sh
# CUDA 12.5
export PATH=/usr/local/cuda-12.5/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.5/lib64

# PSRDADA
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

# Poetry
export PATH="/home/obs/.local/bin:$PATH"
# Fix the "Poetry: Failed to unlock the collection" issue
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

# Added automatically in the Rust installation process
. "$HOME/.cargo/env"
```