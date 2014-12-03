" File: AutoFileSync.vim
" Author: erxiao.chen.gd@gmail.com
" Description: The synchronized file solution for Vim
"
" Testing Info:

if exists('did_AutoFileSync_plugin') || &cp || version < 700
    finish
endif

" The Commands we define.
command! -bar AutoFileSyncAllFiles     cal AutoFileSync#syncAllFiles()
command! -bar AutoFileSyncSingleFile   cal AutoFileSync#syncFile()

augroup AutoFileSync
    au!
    autocmd BufWritePost,FileWritePost * call AutoFileSync#syncFile()
    "au CursorMovedI * call UltiSnips#CursorMoved()
    "au CursorMoved * call UltiSnips#CursorMoved()
    "au BufLeave * call UltiSnips#LeavingBuffer()
    "au InsertLeave * call UltiSnips#LeavingInsertMode()
augroup END

call AutoFileSync#map_keys#MapKeys()

let did_AutoFileSync_plugin=1

" vim: ts=8 sts=4 sw=4
