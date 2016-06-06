function select_city(){
   var url = "index.php";
   var s_city = document.getElementById("s_city");
   var i = s_city.selectedIndex;
   if(i > 0){
      url += "?city=" + s_city.options[i].text;
   }
   location.href = url;
}

function filter(){
  var str_url="index.php?filter=1";
  var s_rname = document.getElementById("rname");
  var s_isp = document.getElementById("isp");
  var s_rtt = document.getElementById("rtt");
  var s_tip = document.getElementById("tip").value;
  var s_tdes = document.getElementById("tdes").value;

  i = s_rname.selectedIndex;
  if(i > 0){str_url += "&rname="+s_rname.options[i].value;}
  i = s_isp.selectedIndex;
  if(i > 0){str_url += "&isp="+s_isp.options[i].value;}
  i = s_rtt.selectedIndex;
  if(i > 0){str_url += "&status="+s_rtt.options[i].value;}
  if(s_tip != "互联地址" && s_tip !=""){
     str_url += "&tip="+s_tip;
  }
  if(s_tdes != "单位名称" && s_tdes != ""){
     str_url += "&tdes="+s_tdes;
  }

  location.href = str_url;
}

function clear_filter(){
  var str_url="index.php?clear=1";
  //alert(str_url);
  location.href = str_url;
}

function change_row_number(){
  var se = document.getElementById("rowNumber");
  var i = se.selectedIndex;
  if(i > 0){
    var rnum = se.options[i].value;
    location.href = "index.php?rnum="+rnum;
  }
}

function add_show(){
  document.getElementById("rec_add").style.display="inline";
}

var xhr = null;
var data_add = new Array();
var data_edit = new Array();

function check_ip(ip){
  var reg=/^(([01]?[\d]{1,2})|(2[0-4][\d])|(25[0-5]))(\.(([01]?[\d]{1,2})|(2[0-4][\d])|(25[0-5]))){3}$/;
  if(reg.test(ip)){
    return true;
  }else{
    return false;
  }
}

function check_tdes(str){
  //var reg=/^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9])+((DX)|(HS)|(LT)|(YD))$/;
  //var reg=/((DX)|(HS)|(LT)|(YD))$/;
  if(str == '' || str.length > 20){return false;}
  var reg = /((or)|(OR)|(\|)|(\\)|(dele)|(DELE)|(inse)|(INSE)|(upd)|(UPD))/;
  if(reg.test(str)){
    return false;
  }else{
    return true;
  }
}

function add_check(){
   var a_rname = document.getElementById("rname_add");
   var a_isp = document.getElementById("isp_add");
   var a_tip = document.getElementById("tip_add").value;
   var a_tdes = document.getElementById("tdes_add").value;
   i = a_rname.selectedIndex;
   j = a_isp.selectedIndex;
   //alert(check_tdes(a_tip));
   if(i > 0){
      if(j > 0){
	      if(a_tip!="" && check_ip(a_tip)){
	         //if(a_tdes!="" && a_tdes.length<20){
            if(check_tdes(a_tdes)){
               //alert(a_tdes);
	            data_add[0] = a_rname.options[i].value;
	            data_add[1] = a_tdes;
	            data_add[2] = a_tip;
	            data_add[3] = a_isp.options[j].value;
	            return true;
	         }else{
	            document.getElementById("result").innerHTML="请检查单位名称";
	            return false;
	         }
	      }else{
	         document.getElementById("result").innerHTML="请检查互联IP";
	         return false;
	      }
      }else{
	      document.getElementById("result").innerHTML="请选择运行商";
	      return false;
      }
   }else{
      document.getElementById("result").innerHTML="请选择接入点";
      return false;
   }
}
	  
function edit_check(){
  var e_rname = document.getElementById("rname_edit");
  var e_isp = document.getElementById("isp_edit");
  var e_pri = document.getElementById("alert_edit");
  var e_tip = document.getElementById("tip_edit").value;
  var info  = document.getElementById("edit_info");
  i = e_rname.selectedIndex;
  j = e_isp.selectedIndex;
  k = e_pri.selectedIndex;
  if(i > 0){
    if(j > 0){
      if(k > 0){
	if(e_tip!="" && check_ip(e_tip)){
	  data_edit[0] = e_tip;
	  data_edit[1] = e_rname.options[i].value;
	  data_edit[2] = e_isp.options[j].value;
	  data_edit[3] = e_pri.options[k].value;
	  return true;
	}else{
	  info.innerHTML="请检查IP格式";
	  return false;
	}
      }else{
	info.innerHTML="请检查告警开关";
	return false;
      }
    }else{
      info.innerHTML="请选择运行商";
      return false;
    }
  }else{
    info.innerHTML="请选择接入点";
    return false;
  }
}

function ajax_add_target(){
  if(add_check()){
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	      document.getElementById("result").innerHTML=xhr.responseText;
	      //var url1="index.php?filter=1&tdes="+data_add[1];
         var url1="index.php?filter=1";
	      var t=setTimeout("location.href='"+url1+"'",2000);
      }
    } 
    var url = "ajax/ajax_add_target.php?rname="+data_add[0]+"&tdes="+data_add[1];
    url = url + "&tip="+data_add[2]+"&isp="+data_add[3];
    //alert(url);
    //使用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url);
    //alert(url);
    xhr.open("POST",url,true);
    xhr.send();
  }
}

function ajax_rm_target(obj){
  var warn="确定要删除["+obj.name+"]吗?";
  var r=confirm(warn);
  if(r){
    var url = "ajax/ajax_rm_target.php?tdes=" + obj.name;
    //使用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url); 
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	      alert(xhr.responseText);
	      history.go(0);	//刷新页面
      }
    }

    xhr.open("GET",url,true);
    xhr.send();
  }
}

function ajax_det_target(tdes){
    var url = "ajax/ajax_det_target.php?tdes=" + tdes;
    //使用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url); 
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	      alert(xhr.responseText);
      }
    }

    xhr.open("GET",url,true);
    xhr.send();
}

function edit_confirm(tdes){
  if(edit_check()){
      var phone=document.getElementById("phone").value;
      var mail1=document.getElementById("mail1").value;
      var mail2=document.getElementById("mail2").value;
      mail1 = jstrim(mail1);
      mail2 = jstrim(mail2);
      phone = jstrim(phone);
      if(phone != '' && !check_phone(phone)){
         alert(phone + ':请检查手机号码格式！');
         return;
      }else{
         //alert(phone + '号码格式正确');
      }
      if(mail1 != '' && !check_mail(mail1)){
         alert(mail1 + ':请检查邮箱地址格式！');
         return;
      }else{
         //alert(mail1 + '邮箱格式正确');
      }
      if(mail2 != '' && !check_mail(mail2)){
         alert(mail2 + ':请检查邮箱地址格式！');
         return;
      }else{
         //alert(mail2 + '邮箱格式正确');
         //return;
      }

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	     alert(xhr.responseText);
	     history.back();
      }
    } 
    var url = "ajax/ajax_edit_target.php?rname="+data_edit[1]+"&tdes="+tdes
      + "&tip="+data_edit[0]+"&isp="+data_edit[2]+"&alert="+data_edit[3];
    url = url + "&mail1=" + mail1;
    url = url + "&mail2=" + mail2;
    url = url + "&phone=" + phone;
    //用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url);
    xhr.open("GET",url,true);
    xhr.send();
    
  }
}

function ajax_edit_detail(tdes){
    //alert(tdes);
    var line_no=document.getElementById("line_no").value; 
    var isp_contact=document.getElementById("isp_contact").value; 
    var t_address=document.getElementById("t_address").value; 
    var t_contact=document.getElementById("t_contact").value; 
    var app_name=document.getElementById("app_name").value; 
    var app_contact=document.getElementById("app_contact").value; 
    var line_fee=document.getElementById("line_fee").value; 
    var line_own=document.getElementById("line_own").value; 
    var memo=document.getElementById("memo").value; 

    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	     alert(xhr.responseText);
	     history.back();
      }
    } 
    var url = "ajax/ajax_edit_detail.php?tdes=" + tdes;
    url = url + "&line_no=" + line_no;
    url = url + "&isp_contact=" + isp_contact;
    url = url + "&t_address=" + t_address;
    url = url + "&t_contact=" + t_contact;
    url = url + "&app_name=" + app_name;
    url = url + "&app_contact=" + app_contact;
    url = url + "&line_fee=" + line_fee;
    url = url + "&line_own=" + line_own;
    url = url + "&memo=" + memo;
    //用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url);
    //alert(url);
    xhr.open("GET",url,true);
    xhr.send();
    
}

function edit_cancel(){
  history.back();
}

function login(){
 var usr=document.getElementById("username"); 
 var pwd=document.getElementById("passwd").value;
 pwd = hex_md5(pwd);
 //alert(pwd);
 if(usr.value!=""){ 
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
	     if(xhr.responseText=='1'){
	       history.go(0);
	     }else{
	       usr.value="用户名或密码错误";
	     }
      }
    }
    var url="ajax/ajax_login.php?usr="+usr.value+"&pwd="+pwd;
    xhr.open("GET",url,true);
    xhr.send();
  }
}

function logout(){ 
  xhr = new XMLHttpRequest();
  xhr.onreadystatechange=function(){
    if(xhr.readyState==4 && xhr.status==200){
//      alert(xhr.responseText);
      history.go(0);
    }
  }
  var url="ajax/ajax_logout.php";
  xhr.open("GET",url,true);
  xhr.send();

}


function chpwd(){
   var old=document.getElementById("pwd_old").value;
   var new1=document.getElementById("pwd_new1").value;
   var new2=document.getElementById("pwd_new2").value;
   if(new1.length > 3 && old.length > 3){
      if(new1 == new2){
         xhr = new XMLHttpRequest();
         xhr.onreadystatechange=function(){
            if(xhr.readyState==4 && xhr.status==200){
               alert(xhr.responseText);
               history.go(0);
            }
         }
         old=hex_md5(old);
         new1=hex_md5(new1);
         var url="ajax/ajax_chpwd.php?pwd="+old+"&new="+new1;
         xhr.open("GET",url,true);
         xhr.send();
      }else{
         alert("两次输入新密码不一致!");
      }
   }else{
      alert("密码不能少于4位!");
   }
}

function sw_alert(str_city){
   var s_alert = document.getElementById("alert_sw");
   var i = s_alert.selectedIndex;
   if(i > 0){
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
         }
      }
      var url="ajax/ajax_sw_alert.php?city="+str_city+"&pri="+s_alert.options[i].value;
      //alert(url);
      url = encodeURI(url);
      xhr.open("GET",url,true);
      xhr.send();
   }
} 

//去掉字符串空格
function jstrim(str){
   var i=0;
   var len=str.length;
   trimstr="";
   while(i<len){
      if(str.charAt(i)!=" "){
         trimstr=trimstr+str.charAt(i);
      }
      i++;
   }
   return(trimstr);
}

function check_phone(str){
  var t_str = str.split(';');
  //手机号码正则匹配
  var reg=/^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
  for(var i=0,len=t_str.length; i<len; i++){
     if(t_str[i]!='' && !reg.test(t_str[i]))
        return false;
  }
  return true;
}

function check_mail(str){
  var t_str = str.split(';');
  //邮箱地址正则匹配
  var reg=/^(((\w)+(\.\w+)*@(\w)+((\.\w+)+))|(\w+(\/\w+)+\/ccb))$/;
  for(var i=0,len=t_str.length; i<len; i++){
     if(t_str[i]!='' && !reg.test(t_str[i]))
        return false;
  }
  return true;
}

function chmail(){
   var note = "请分别填写手机号码、内外网邮箱(可以留空)\n填写多个号码、邮箱请以';'(英文分号)分隔";
   var r=confirm(note);
   if(r){
      var phone=document.getElementById("phone").value;
      var mail1=document.getElementById("mail1").value;
      var mail2=document.getElementById("mail2").value;
      mail1 = jstrim(mail1);
      mail2 = jstrim(mail2);
      phone = jstrim(phone);
      if(phone != '' && !check_phone(phone)){
         alert(phone + ':请检查手机号码格式！');
         return;
      }else{
         //alert(phone + '号码格式正确');
      }
      if(mail1 != '' && !check_mail(mail1)){
         alert(mail1 + ':请检查邮箱地址格式！');
         return;
      }else{
         //alert(mail1 + '邮箱格式正确');
      }
      if(mail2 != '' && !check_mail(mail2)){
         alert(mail2 + ':请检查邮箱地址格式！');
         return;
      }else{
         //alert(mail2 + '邮箱格式正确');
         //return;
      }

      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
         }
      }
      var url="ajax/ajax_chmail.php?mail1="+mail1+"&mail2="+mail2;
      url = url + '&phone=' + phone;
      //alert(url);
      xhr.open("GET",url,true);
      xhr.send();
   }
}


function add_device(obj){
   var vendor = document.getElementById("s_vendor");
   var output = document.getElementById("txt_out");
   var dname = document.getElementById("txt_dname");
   var dip = document.getElementById("txt_ip");
   var proto = document.getElementById("s_proto");
   var auth = document.getElementById("s_auth");
   var i = vendor.selectedIndex;
   var j = proto.selectedIndex;
   var k = auth.selectedIndex;
   if(i == 0){
      output.innerHTML = '请选择厂商';
      return false;
   }
   if(check_dname(dname.value) == false){
      output.innerHTML = '合法设备名称由大小写字母、下划线、数字组成';
      return false;
   }
   if(check_ip(dip.value) == false){
      output.innerHTML = '请检查IP地址格式';
      return false;
   }
   if(j == 0){
      output.innerHTML = '请选择协议';
      return false;
   }
   if(k == 0){
      output.innerHTML = '请选择登陆方式';
      return false;
   }
   var pass1 = document.getElementById("pass1").value;
   var pass2 = document.getElementById("pass2").value;
   var pass3 = document.getElementById("pass3").value;
   if(pass1 == '' || pass2 == '' || pass3 == ''){
      output.innerHTML = '合法用户名密码不能为空';
      return false;
   }

   var mode = proto.options[j].value + vendor.options[i].value;
   var login = parseInt(mode) * 10 + parseInt(auth.options[k].value);
   //alert(login);
   obj.disabled = true;
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         alert(xhr.responseText);
         obj.disabled = false;
         history.go(0);
         //output.innerHTML = xhr.responseText;
         //var t=setTimeout("history.go(0)",2000);
      }
   }
   var url = "ajax/ajax_add_router.php?rip=" + dip.value;
   url = url + "&rname=" + dname.value;
   url = url + "&pass1=" + encodeURIComponent(pass1);
   url = url + "&pass2=" + encodeURIComponent(pass2);
   url = url + "&pass3=" + encodeURIComponent(pass3);
   url = url + "&corp=" + vendor.options[i].text;
   url = url + "&mode=" + login;
   url = url + "&app=2";
   //alert(url);
   xhr.open("GET",url,true);
   xhr.send();

   return true;
}

function input_pass(obj){
   var i = obj.selectedIndex;
   var output = document.getElementById("txt_out");
   if(i == 0){
      output.innerHTML = '请选择登陆方式';
      return false;
   }
   var p_pass = document.getElementById("pass");
   var strhtml = '1<input type="password" id="pass1" size="8">';
   strhtml = strhtml + '2<input type="password" id="pass2" size="8">';
   if(i == 1){
      strhtml = strhtml + '3<input type="password" id="pass3" size="8">';
   }else{
      strhtml = strhtml + '<input id="pass3" size="2" value="notnull" disabled=true hidden>';
   }
   p_pass.innerHTML = strhtml;
   return true;
}

function rm_device(ip){
   var msg= "确定删除设备[" + ip + "]吗?"
   var r=confirm(msg);
   if(r){
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
            history.go(0);
         }
      }
      var url = "ajax/ajax_del_router.php?ip=" + ip;
      url = url + "&app=2";
      xhr.open("GET",url,true);
      xhr.send();
      //
   }

}

function check_dname(str){
  if(str.length > 20)
    return false;
  //var reg=/^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9])+((DX)|(HS)|(LT)|(YD))$/;
  //var reg=/^w+$/;
  var reg=/^[A-Za-z0-9_]+$/;
  if(reg.test(str)){
    return true;
  }else{
    return false;
  }
}

function ajax_save_conf(obj, ip){
   var msg = "手动保存一次配置(系统每月自动保存)\n";
   msg = msg + "某些设备保存时间较长，请耐心等待";
   var r = confirm(msg);
   if(r){
      obj.disabled = true;
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
            obj.disabled = false;
         }
      }
      var url = "ajax/ajax_save_conf.php?ip=" + ip;
      xhr.open("GET",url,true);
      xhr.send();
      //
   }
}

function ajax_test_login(obj, ip){
   var msg = "尝试登陆设备["+ip+"]，继续？";
   var r = confirm(msg);
   if(r){
      obj.disabled = true;
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
            obj.disabled = false;
         }
      }
      var url = "ajax/ajax_test_login.php?ip=" + ip;
      xhr.open("GET",url,true);
      xhr.send();
      //
   }
}

function operate(obj, ip){
   // alert(ip);
   var i = obj.selectedIndex;
   if(i == 0){
      return;
   }
   switch(i){
      case 1:
         ajax_test_login(obj, ip);
         break;
      case 2:
         ajax_save_conf(obj, ip)
         break;
      case 3:
         url = "StateCheck.php?ip=" + ip;
         location.href = url;
         break;
      case 4:
         rm_device(ip);
         break;
      default:
         alert('选择操作任务失败');
   }


}
