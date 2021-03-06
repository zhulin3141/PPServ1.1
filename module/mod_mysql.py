#!/usr/bin/env python
# coding:utf-8

from common import *
from base_module import BaseModule
from lang import *
import wx
from configobj import ConfigObj

class Mod_Mysql(BaseModule):
    '''Mysql模块类'''
    def __init__(self, name):
        BaseModule.__init__(self, name)
        self.conf_file = BASE_DIR + self.path + "\my.ini"
        self.parse_config_file()

        self.cfg_ctr = {}

    def parse_config_file(self):
        self.content = open(self.conf_file,'r').read()

        self.cfg = ConfigObj(self.conf_file)

    def set_advt_frame(self, parent):
        self.setting_panel = wx.Panel(parent)
        self.setting_panel.SetSizer(self.setting_sizer)

        self.opt_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer = wx.FlexGridSizer(rows=15, cols=4)

        for cfg_name in self.cfg['mysqld'].keys():
            lbl = wx.StaticText(self.setting_panel, -1, cfg_name)
            self.cfg_ctr[cfg_name] = txt = wx.TextCtrl(self.setting_panel, -1, self.cfg['mysqld'][cfg_name], size=(200, 20))
            self.grid_sizer.Add(lbl, 0, wx.ALL, 5)
            self.grid_sizer.Add(txt, 0, wx.ALL, 3)

        log_btn = wx.Button(self.setting_panel, -1, Lang().get('open_log_file'))
        log_btn.Bind(wx.EVT_BUTTON, self.open_log_file)

        conf_btn = wx.Button(self.setting_panel, -1, Lang().get('mysql_config_file'))
        conf_btn.Bind(wx.EVT_BUTTON, self.open_config_file)

        console_btn = wx.Button(self.setting_panel, -1, Lang().get('console'))
        console_btn.Bind(wx.EVT_BUTTON, self.open_console)

        save_btn = wx.Button(self.setting_panel, -1, Lang().get('save_config'))
        save_btn.Bind(wx.EVT_BUTTON, self.save_config)

        self.handler_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.handler_sizer.AddMany([
            (log_btn),
            (conf_btn),
            (console_btn),
            (save_btn)
        ])

        self.opt_sizer.Add(self.grid_sizer)
        self.opt_sizer.Add(self.handler_sizer, 0, wx.TOP, 5)
        self.setting_sizer.Add(self.opt_sizer, 0, wx.ALL, 5)

        parent.AddPage(self.setting_panel, self.module_name)

    def open_log_file(self, event):
        open_file(self.cfg['mysqld']['log-error'])

    def open_config_file(self, event):
        open_file(self.conf_file)

    def save_config(self, event):
        #保存配置
        for cfg_name, ctr in self.cfg_ctr.items():
            self.cfg['mysqld'][cfg_name] = ctr.GetValue()
        self.cfg.write()

    def open_console(self, event):
        open_cmd(self.path + '\\bin', 'mysql -u root -p')
