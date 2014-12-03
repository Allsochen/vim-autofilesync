vim-autofilesync
================

A plugin which can synchronize file to other directly automatically for vim

## Installation
This assumes you are using [Vundle](https://github.com/gmarik/Vundle.vim). Adapt
for your plugin manager of choice. Put this into your `.vimrc`.

    " Track the engine.
    Plugin 'Allsochen/vim-autofilesync'

## Basic Usage
* Run `:AutoFileSyncAllFiles` to invoke AutoFileSync plugin to synchronize all the project files to target path.
* Run `:AutoFileSyncSingleFile` or `:w` to invoke AutoFileSync plugin to synchronize the current open file to target path.
