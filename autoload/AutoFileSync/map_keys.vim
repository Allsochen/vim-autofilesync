" File: AutoFileSync.vim
" Author: erxiao.chen.gd@gmail.com
" Description: The synchronize file solution for Vim

call AutoFileSync#bootstrap#Bootstrap()

function! AutoFileSync#map_keys#MapKeys()
    if !exists('g:python')
        " Do not map keys if bootstrapping failed (e.g. no Python).
        return
    endif

    " Map the keys correctly
    if exists("g:autofilesync_syncAllFiles")
        exec "snoremap <silent> " . g:autofilesync_syncAllFiles . "  <Esc>:call AutoFileSync#syncAllFiles()<cr>"
    endif
endf
