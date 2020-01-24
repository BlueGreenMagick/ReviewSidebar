#addon name cannot contain $
#hook parameter should not contain $
#designator should not contain {} and :
#value should not contain {}

import re
import json

from aqt import mw



FIELD_NAME = "_ReviewSidebar"
VERSION = 10

SIDEBAR_HTML = """
<div id="sidebarBtnsList"> 
  <button class="sidebarBtn" onclick="clickedSidebarButton()">☰</button>
</div>
<div id="revSidebar">
    Loading... Please Wait
</div>
<div id="main">
</div>
"""


def _onProfileLoaded():
    if mw.addonReviewSidebarVer == VERSION and not hasattr(mw, "addonReviewSidebar"):
        mw.addonReviewSidebar = ReviewSidebar()

def initReviewSidebar(func):
    if not hasattr(mw, "addonReviewSidebarFuncs"):
        mw.addonReviewSidebarFuncs = []
    mw.addonReviewSidebarFuncs.append(func)
    if not hasattr(mw, "addonReviewSidebarVer") or mw.addonReviewSidebarVer < VERSION:
        mw.addonReviewSidebarVer = VERSION
        addHook("profileLoaded", _onProfileLoaded)
        
def _linkHandler(self, url, _old):
    if url.startswith("addonReviewSidebar_open_tab$$"):
        (cmd, v) = url.split("$$")
        (desg, val) = v.split("{}")
        mw.addonReviewSidebar._currTab.desg = desg
        mw.addonReviewSidebar._currTab.val = val
        self.mw.addonReviewSidebar._tab_open()
    elif url.startswith("addonReviewSidebar_runhook$$"):
        msg = url.split("$$")
        (cmd, addon_name, hookstr) = msg[0:3]
        self.mw.addonReviewSidebar.hooks[addon_name][hookstr](*msg[3:])
    else:
        return _old(self, url)

def _onRevHtml(self, _old):
    mw.addonReviewSidebar._currTabDesg = "" #remove desg from prev review session
    html = mw.addonReviewSidebar.on_rev_html()
    return _old(self) + html

def _showQuestion(self, *arg, **kwargs):
    mw.addonReviewSidebar._on_new_page()

class ReviewSidebar():

    """
        functions:
            add_designator
            on_tab_open
            on_rev_html
            get_current_tab
            add_hook
            set_html
            execute_js
    
    """


    def __init__(self):
        if hasattr(mw, "addonReviewSidebar"):
            raise Exception("ERROR: Don't make a ReviewSidebar instance directly. Call initReviewSidebar() instead")
        self.desgs = {}
        self.hooks = {}
        self.on_tab_open_funcs = {}
        self.rev_html_per_addon = {}
        self.version = VERSION
        self.field_name = FIELD_NAME
        self._currTab = {
            "desg": "",
            "val": ""
        }

    def add_designator(self, addon_name, desg, icon_path = None):
        if desg in self.desgs:
            raise Exception("ERROR: Multiple ReviewSidebar addons sharing same designator! \naddon1:'{}'\naddon2:'{}'".format(self.desgs[desg], __name__))
        addon_name = addon_name.split(".")[0]
        self.desgs[desg] = [addon_name, icon_path]
    
    def on_tab_open(self, addon_name, func):
        addon_name = addon_name.split(".")[0]
        self.on_tab_open_funcs[addon_name] = func

    def _tab_open(self):
        desg = self._currTab["desg"]
        val = self._currTab["val"]
        addon_name = self.desgs[desg][0]
        on_tab_open_funcs[addon_name](desg, val)

    def on_rev_html(self, addon_name, html):
        addon_name = addon_name.split(".")[0]
        self.rev_html_per_addon[addon_name] = html

    def _on_rev_html(self):
        html = SIDEBAR_HTML
        for a in self.rev_html_per_addon:
            self.rev_html_per_addon[a]

    def set_html(self, desg, val, html):
        if mw.state == "review" and self._currTab.desg = desg and self._currTab.val = val:
            mw.reviewer.web.eval("reviewSidebarSetHtml({})".format(json.dumps(html)))

    def execute_js(self, desg, val, js):
        if mw.state == "review" and self._currTab.desg = desg and self._currTab.val = val:
            mw.reviewer.web.eval(js)

    def get_current_tab(self):
        """
            Returns currently open tab designator in review window.
            If no tab is open, or not in review mode, return ""
        """
        if mw.state == "review":
            return self._currTab
        else:
            empty = {
                "desg": "",
                "val": ""
            }
            return empty

    def add_hook(self, addon_name, hookstr, hookfn):
        self.hooks[addon_name][hookstr] = hookfn

    def _run_hook(self, addon_name, hookstr, *args):
        self.hooks[addon_name][hookstr](*args)

    def _process_field(self, fld):
        ms = re.findall("{(?:[^:]+?):(?:[\s\S]+?)}", fld)
        for i, m in enumerate(ms):
            ms[i] = m.split(":", 1)
        return ms

    def _makeSidebarTabList(self, fldv):
        tabs = []
        for m in fldv:
            desg = m[0]
            val = m[1]
            addon_name = self.desgs[desg][1]
            icon_path = self.desgs[desg][2]
            tabs.append([desg, val, addon_name, icon_path])
        return tabs
    
    def _on_new_page(self):
        self._currTab.desg = ""
        self._currTab.val = ""
        self._list_tab()

    def _list_tab(self):
        rev_note = mw.reviewer.card.note()
        fldnm = self.field_name
        if fldnm in rev_note:
            fldv = _process_field(rev_note[fldnm])
            self._fldv = fldv
            tabs = _makeSidebarTabList(fldv)
        else:
            tabs = []
        mw.reviewer.web.eval("nextCard();")
        mw.reviewer.web.eval("reviewSidebarListTabs({});").format(json.dumps(tabs))

    def _onProfileLoaded(self):
        Reviewer._linkHandler = wrap(Reviewer._linkHandler, _linkHandler, "around")
        Reviewer.revHtml = wrap(Reviewer.revHtml, _onRevHtml, "around")
        Reviewer._showQuestion = wrap(Reviewer._showQuestion, _showQuestion, "before")
        
