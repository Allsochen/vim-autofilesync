#!/usr/bin/env python
# encoding: utf-8

"""Entry point for all thinks AutoFileSync."""

import vim  # pylint:disable=import-error

from AutoFileSync.autofilesync_manager import AutoFileSyncManager

options = dict(configFileName = vim.eval('g:autofilesync_configFileName'),
               findConfigFileDepth = vim.eval('g:autofilesync_findConfigFileDepth'),
               projectSearchPaths = vim.eval('g:autofilesync_projectSearchPaths'))
AutoFileSync_Manager = AutoFileSyncManager(options)# pylint:disable=invalid-name
