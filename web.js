function nextCard(){
  closeSidebar()
  window.revSidebarCurr = {
    "desg": "",
    "addonNm": "",
    "val": ""
  }
}


function clickedSidebarBtn(tab){
  var desg = t[0];
  var val = t[1]
  var addonNm = t[2];
  var icnpth = t[3];
  var loadingMsg = "Loading... Please Wait";

  if(revSidebarCurr.desg == desg && revSidebarCurr.val == val){
    revSidebarCurr.desg = "";
    revSidebarCurr.addonNm = "";
    revSidebarCurr.val = ""
    curTabStr = revSidebarCurr.desg + "{}" + revSidebarCurr.val
    pycmd("addonReviewSidebar_open_tab$$" + curTabStr)
    closeSidebar();
    document.getElementById("revSidebar").innerHTML = loadingMsg;
  }else{
    var prevTab = revSidebarCurr
    revSidebarCurr.desg = desg;
    revSidebarCurr.addonNm = addonNm;
    revSidebarCurr.val = val
    curTabStr = revSidebarCurr.desg + "{}" + revSidebarCurr.val
    document.getElementById("revSidebar").innerHTML = loadingMsg;
    pycmd("addonReviewSidebar_open_tab$$" + curTabStr)
    if(prevTab.desg == ""){
      openSidebar()
    }
  }
}

function openSidebar(){
    width = "500px"
    document.getElementById("revSidebar").style.width = width;
    document.getElementById("sidebarBtnsList").style.marginRight = width;
    document.getElementById("qa").style.marginRight = width;
}

function closeSidebar(){
    document.getElementById("noteContextSidebar").style.width = "0";
    document.getElementById("sidebarBtnsList").style.marginRight = "0";
    document.getElementById("qa").style.marginRight = "0";
}

function reviewSidebarSetHtml(html){
  html = JSON.parse(html)
  document.getElementById("revSidebar").innerHTML = html
}

function reviewSidebarListTabs(data){
  var tabs = JSON.parse(data);
  var totBtnHtml = "";
  for(var x = 0; x < tabs.length; x++){
    var t = tabs[x];
    var desg = t[0];
    var val = t[1]
    var addonNm = t[2];
    var icnpth = t[3];

    //create button
    var btnsDiv = document.getElementById("sidebarBtnsList");
    var btnEl = document.createElement("btn");
    if(icnpth == ""){
      icnTxtElm = document.createElement("div");
      icnTxtElm.innerHTML = desg[0]
      icnTxtElm.classList.add("sidebarBtnTxt")
      btnEl.appendChild(icnTxtElm)
    }else{
      icnElm = document.createElement("img");
      icnElm.src = icnpth;
      icnElm.classList.add("sidebarBtnImg");
      btnEl.appendChild(icnElm);
    }
    btnEl.classList.add("sidebarBtn");
    btnEl.onclick = function(){
      clickedSidebarBtn(t);
    }
    btnsDiv.appendChild(btnEl);
  }
}

function runHook(){
  args = Array.prototype.slice.call(arguments);
  pycmd("addonReviewSidebar_runhook$$" + revSidebarCurrAddon + "$$" + args.join("$$"));
}