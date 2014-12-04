call AutoFileSync#bootstrap#Bootstrap()

function! AutoFileSync#map_keys#MapKeys()
    if !exists('g:python')
        " Do not map keys if bootstrapping failed (e.g. no Python).
        return
    endif

    " Map the keys correctly
    if exists("g:autofilesync_syncAllFiles")
        exec "nmap <silent> " . g:autofilesync_syncAllFiles . " :call AutoFileSync#syncAllFiles()<cr>"
    else
        exec "nmap <silent> <F6> :call AutoFileSync#syncAllFiles()<cr>"
    endif

    if exists("g:autofilesync_syncUpdateFiles")
        exec "nmap <silent> " . g:autofilesync_syncUpdateFiles . " :call AutoFileSync#syncUpdateFiles()<cr>"
    else
        exec "nmap <silent> <F7> :call AutoFileSync#syncUpdateFiles()<cr>"
    endif
endf
