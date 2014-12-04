let s:SourcedFile=expand("<sfile>")

function! AutoFileSync#bootstrap#Bootstrap()
   if exists('s:did_AutoFileSync_bootstrap')
      return
   endif
   let s:did_AutoFileSync_bootstrap=1

   if !exists("g:AutoFileSyncUsePythonVersion")
       let g:python=":py3 "
       if !has("python3")
           if !has("python")
               if !exists("g:AutoFileSyncNoPythonWarning")
                   echo  "AutoFileSync requires py >= 2.6 or any py3"
               endif
               unlet g:python
               return
           endif
           let g:python=":py "
       endif
       let g:AutoFileSyncUsePythonVersion = "<tab>"
   else
       if g:AutoFileSyncUsePythonVersion == 2
           let g:python=":py "
       else
           let g:python=":py3 "
       endif
   endif

   " Expand our path
   exec g:python "import vim, os, sys"
   exec g:python "sourced_file = vim.eval('s:SourcedFile')"
   exec g:python "while not os.path.exists(os.path.join(sourced_file, 'pythonx')):
      \ sourced_file = os.path.dirname(sourced_file)"
   exec g:python "module_path = os.path.join(sourced_file, 'pythonx')"
   exec g:python "vim.command(\"let g:AutoFileSyncPythonPath = '%s'\" % module_path)"
   exec g:python "if not hasattr(vim, 'VIM_SPECIAL_PATH'): sys.path.append(module_path)"
   exec g:python "from AutoFileSync import AutoFileSync_Manager"
endfunction

" Config the the project where you want to sync.
if !exists("g:autofilesync_configFileName")
    " The configuration just as follow:
    " {
    "    "target": "Y:\\home\\allsochen\\projects\\MTT\\TestServer",
    "    "excludesSuffix": [".svn"]
    "    "excludesPaths": [".syncfilesync", ".svn"]
    " }
    let g:autofilesync_configFileName = "autofilesync.json"
endif

" Config the depth for current editting file to project config file.
" If not found the project config file, it will not auto sync.
if !exists("g:autofilesync_findConfigFileDepth")
    let g:autofilesync_findConfigFileDepth = 5
endif

" Enable the AutoFileSync function for project path.
if !exists("g:autofilesync_projectSearchPaths")
    let g:autofilesync_projectSearchPaths = ["D:\\Codes"]
endif

" Enable the AutoFileSync future.
if !exists("g:autofilesync_enable")
    let g:autofilesync_enable = "true"
endif

call AutoFileSync#bootstrap#Bootstrap()
