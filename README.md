vim-autofilesync
================

A plugin which can synchronize file to other directly automatically for vim

## Installation
This assumes you are using [Vundle](https://github.com/gmarik/Vundle.vim). Adapt
for your plugin manager of choice. Put this into your `.vimrc`.

    " Track the engine.
    Plugin 'Allsochen/vim-autofilesync'
Add `syncfilesync.json` file into your project root path, the content of syncfilesync.json is as followed:

    " dest: the target path you want to sync to.
    " excludeSuffix: exclude the file ends with this suffix.
    " excludePaths: exclude the path like this suffix, suported regular expression.
    {
        "dest": ""Y:\\home\\allsochen\\projects\\Circle\\CircleProxyServer",
        "excludesSuffix": [".svn"],
        "excludesPaths": [".svn", ".svn-base", "autofilesync.json"]
    }

## Configuration
Put this into your `.vimrc` to control different action.

    " The configuration file specified the project where you want to sync.
    " default is autofilesync.json file
    let g:autofilesync_configFileName = autofilesync.json
    
    " Config the depth for current editting file to project config file.
    " If not found the project config file `g:autofilesync_configFileName`
    " in base project path it will not auto sync.
    let g:autofilesync_findConfigFileDepth = 5
    
    " Enable the AutoFileSync feture for project.
    " Advice you add this to `.vimrc` to avoid additional sync operation
    " when edit a file not in a project.
    let g:autofilesync_projectSearchPaths = ["D:\\Codes"]

## Basic Usage
* Run `:AutoFileSyncAllFiles` to invoke AutoFileSync plugin to synchronize all the project files to target path.
* Run `:AutoFileSyncUpdateFiles` to invoke AutoFileSync plugin to synchronize all the modified project files to target path.
* Run `:AutoFileSyncSingleFile` or `:w` to invoke AutoFileSync plugin to synchronize the current open file to target path.
* Run `:AutoFileSyncEnable` disable AutoFileSync plugin.
* Run `:AutoFileSyncDisable` to disable AutoFileSync plugin.
* You can use `let g:autofilesync_syncAllFiles = "<c-y>"` to bind a key map for `:AutoFileSyncAllFiles` operation.

