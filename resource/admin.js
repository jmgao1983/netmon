function ajax_add_city(){
  var city=prompt("请输入城市名称", "杭州");
  if(city != "" && city.length < 10){
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
        alert(xhr.responseText);
        history.go(0);
      }
    }
    var url = "admin/ajax_add_city.php?city=" + city;
    //使用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url);
    //alert(url);
    xhr.open("GET",url,true);
    xhr.send();
  }else{
    alert("城市名称为不超过10个汉字!");
  }
}


function ajax_del_city(str_city){
  var r=confirm("确定要删除城市[" + str_city + "]吗？");
  if(r){
    xhr = new XMLHttpRequest();
    xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
        alert(xhr.responseText);
        history.go(0);
      }
    }
    var url = "admin/ajax_del_city.php?city=" + str_city;
    //使用JS直接对URL编码(utf-8),不使用浏览器或者系统的编码规则
    url = encodeURI(url);
    //alert(url);
    xhr.open("GET",url,true);
    xhr.send();
  }
}

function ajax_add_router(obj){
   var vendor = document.getElementById("s_vendor");
   var output = document.getElementById("txt_out");
   var dname = document.getElementById("txt_dname");
   var dip = document.getElementById("txt_ip");
   var proto = document.getElementById("s_proto");
   var auth = document.getElementById("s_auth");
   var city = document.getElementById("s_city");
   var i = vendor.selectedIndex;
   var j = proto.selectedIndex;
   var k = auth.selectedIndex;
   var l = city.selectedIndex;
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
   if(l == 0){
      output.innerHTML = '请选择城市';
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
   url = url + "&city=" + encodeURIComponent(city.options[l].text);
   url = url + "&mode=" + login;
   url = url + "&app=3";
   //alert(url);
   xhr.open("GET",url,true);
   xhr.send();

   return true;
}

function ajax_del_router(ip){
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
      url = url + "&app=3";
      xhr.open("GET",url,true);
      xhr.send();
      //
   }

}

function ajax_add_user(){
   var city = document.getElementById("s_city2");
   var name = document.getElementById("add_user").value;
   var pwd1 = document.getElementById("add_pwd1").value;
   var pwd2 = document.getElementById("add_pwd2").value;
   var output = document.getElementById("user_output");
   var i = city.selectedIndex;
   if(i == 0){
      output.innerHTML = '请选择城市';
      return false;
   }
   if(check_dname(name) == false){
      output.innerHTML = "合法用户名由大小写字母、数字、下划线组成";
      return false;
   }
   if(!(pwd1.length > 0 && pwd1.length < 20 && pwd1 == pwd2)){
      output.innerHTML = "请检查两次密码输入";
      return false;
   }
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         alert(xhr.responseText);
         history.go(0);
      }
    }
   var url="admin/ajax_add_user.php?name="+name+"&pwd="+hex_md5(pwd1);
   url = url + "&city=" + city.options[i].text;
   url = encodeURI(url);
   xhr.open("GET",url,true);
   xhr.send();
}

function ajax_del_user(name){
   var msg= "确定删除用户[" + name + "]吗?"
   var r=confirm(msg);
   if(r){
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
            history.go(0);
         }
      }
      var url = "admin/ajax_del_user.php?name=" + name;
      xhr.open("GET",url,true);
      xhr.send();
      //
   }
}

function test_send_mail(){
   var server = document.getElementById("smtp_server").value;
   var usr = document.getElementById("smtp_usr").value;
   var pwd = document.getElementById("smtp_pwd").value;
   var output = document.getElementById("smtp_output");
   if(server == ''){
      output.innerHTML = '服务器不能为空';
      return false;
   }
   var rev = prompt("请输入收件人邮箱");
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         alert(xhr.responseText);
         //history.go(0);
      }
    }
   var url="admin/test_send_mail.php?server="+server+"&usr="+usr;
   url = url + "&pwd=" + pwd;
   url = url + "&rev=" + rev;
   //url = encodeURI(url);
   //alert(url);
   xhr.open("GET",url,true);
   xhr.send();
}

function save_envi(){
   var log_lvl = document.getElementById("s_loglvl");
   var threads = document.getElementById("s_threads");
   var server = document.getElementById("smtp_server").value;
   var usr = document.getElementById("smtp_usr").value;
   var pwd = document.getElementById("smtp_pwd").value;
   var i = log_lvl.selectedIndex;
   var j = threads.selectedIndex;
   var log = '';
   var thd = '';
   if(i == 0 && server == '' && j == 0){
      alert("设置没有更改！");
      return false;
   }
   if(i > 0){
      log = log_lvl.options[i].value;
   }
   if(j > 0){
      thd = threads.options[j].value;
   }
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         alert(xhr.responseText);
         history.go(0);
      }
   }
   var url = "admin/ajax_save_envi.php?log_lvl=" + log;
   url = url + "&threads=" + thd;
   url = url + "&smtp_server=" + server;
   url = url + "&smtp_usr=" + usr;
   url = url + "&smtp_pwd=" + pwd;
   //alert(url);
   xhr.open("GET",url,true);
   xhr.send();

   return true;
}

function sw_ecnmon(){
   var sw = document.getElementById("sw_ecnmon");
   var i = sw.selectedIndex;
   if(i == 0){
      alert("请选择自动任务");
      return false;
   }
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         alert(xhr.responseText);
         history.go(0);
      }
   }
   var url = "admin/sw_ecnmon.php?sw=" + i;
   //alert(url);
   xhr.open("GET",url,true);
   xhr.send();

   return true;
}


function update_server(obj){
   var msg= "提示:某些版本升级后可能需要额外配置\n确定需要升级版本吗?"
   var r=confirm(msg);
   if(r){
      obj.disabled = true;
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            alert(xhr.responseText);
            obj.disabled = false;
         }
      }
      var url = "admin/update_server.php";
      xhr.open("GET",url,true);
      xhr.send();
      //
   }
}
