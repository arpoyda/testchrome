#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




class Pizda:

    def __init__(self):
        self.driver = self.gen()
        self.driver.get("http://www.whatsmybrowser.org/")

    def create_proxyauth_extension(self, proxy_host, proxy_port,
                                   proxy_username, proxy_password,
                                   scheme='http', plugin_path=None):
        """Proxy Auth Extension
        args:
            proxy_host (str): domain or ip address, ie proxy.domain.com
            proxy_port (int): port
            proxy_username (str): auth username
            proxy_password (str): auth password
        kwargs:
            scheme (str): proxy scheme, default http
            plugin_path (str): absolute path of the extension
        return str -> plugin_path
        """
        import string
        import zipfile

        if plugin_path is None:
            plugin_path = 'add_files\\proxy_auth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
        """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "${scheme}",
                    host: "${host}",
                    port: parseInt(${port})
                  },
                  bypassList: ["foobar.com"]
                }
              };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "${username}",
                    password: "${password}"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path



    def gen(self):
        PROXY_HOST = '217.29.53.187'  # rotating proxy
        PROXY_PORT = 18761
        PROXY_USER = 'a0djqj'
        PROXY_PASS = 'kMjQxy'

        proxyauth_plugin_path = self.create_proxyauth_extension(
            proxy_host=PROXY_HOST,
            proxy_port=PROXY_PORT,
            proxy_username=PROXY_USER,
            proxy_password=PROXY_PASS
        )
        co = Options()
        co.add_argument("--start-maximized")
        co.add_extension(proxyauth_plugin_path)


        return webdriver.Chrome(chrome_options=co)

p = Pizda()