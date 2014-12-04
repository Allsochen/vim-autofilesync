" File: UltiSnips.vim
" Author: Holger Rapp <SirVer@gmx.de>
" Description: The Ultimate Snippets solution for Vim

if exists('did_AutoFileSync_autoload') || &cp || version < 700
    finish
endif
let did_AutoFileSync_autoload=1

call AutoFileSync#bootstrap#Bootstrap()
if !exists("g:python")
   " Delete the autocommands defined in plugin/AutoFileSync.vim and
   augroup AutoFileSync
       au!
   augroup END
   finish
end

" Define dummy version of function called by autocommand setup in
" ftdetect/AutoFileSync.vim and plugin/AutoFileSync.vim.
" If the function isn't defined (probably due to using a copy of vim
" without python support) it would cause an error.
"
function! AutoFileSync#syncFile()
    "try
        exec g:python "AutoFileSync_Manager.syncFile()"
    "catch
        "echomsg "AutoFileSync: sync file error"
    "endtry
endf

function! AutoFileSync#syncUpdateFiles()
    "try
        exec g:python "AutoFileSync_Manager.syncUpdateFiles()"
    "catch
        "echomsg "AutoFileSync: sync update file error"
    "endtry
endf

function! AutoFileSync#syncAllFiles()
    "try
        exec g:python "AutoFileSync_Manager.syncAllFiles()"
    "catch
        "echomsg "AutoFileSync: sync all file error"
    "endtry
endf

function! AutoFileSync#disable()
    let g:autofilesync_enable = "false"
endf

function! AutoFileSync#enable()
    let g:autofilesync_enable = "true"
endf
