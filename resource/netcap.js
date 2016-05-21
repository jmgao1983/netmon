var int1;
var int2;

function cap1(obj, ip){
   clearInterval(int1);
   clearInterval(int2);
   var r=confirm('确定开始设置['+ip+']参照状态吗?');
   if(r){
      obj.disabled = true;
      document.getElementById("btn_cap2").disabled = true;
      document.getElementById("btn_mat").disabled = true;
      var ta = document.getElementById("log_win");
      ta.value += "开始设置[" + ip + "]参照状态\n";
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            ta.value += xhr.responseText;
         }
      }
      var url = "ajax/ajax_cap1.php?ip=" + ip;
      xhr.open("GET",url,true);
      xhr.send();
      //
      var count = 10;
      int1 = setInterval(function(){
         if(count < 0){
            obj.value = '设置参照状态';
            document.getElementById("btn_cap1").disabled = false;
            document.getElementById("btn_cap2").disabled = false;
            document.getElementById("btn_mat").disabled = false;
         }else{
            obj.value = '正在抓取' + count.toString();
         }
         count = count - 1;
      },1000);
   }
}

function cap2(obj, ip){
   clearInterval(int1);
   clearInterval(int2);
   var r=confirm('确定开始抓取['+ip+']当前状态吗?');
   if(r){
      obj.disabled = true;
      document.getElementById("btn_cap1").disabled = true;
      document.getElementById("btn_mat").disabled = true;
      var ta = document.getElementById("log_win");
      ta.value += "开始抓取[" + ip + "]当前状态\n";
      xhr = new XMLHttpRequest();
      xhr.onreadystatechange=function(){
         if(xhr.readyState==4 && xhr.status==200){
            ta.value += xhr.responseText;
         }
      }
      var url = "ajax/ajax_cap2.php?ip=" + ip;
      xhr.open("GET",url,true);
      xhr.send();
      //
      var count = 10;
      int2 = setInterval(function(){
         if(count < 0){
            obj.value = '抓取当前状态';
            document.getElementById("btn_cap1").disabled = false;
            document.getElementById("btn_cap2").disabled = false;
            document.getElementById("btn_mat").disabled = false;
         }else{
            obj.value = '正在抓取' + count.toString();
         }
         count = count - 1;
      },1000);
   }
}

function match(obj, ip){
   clearInterval(int1);
   clearInterval(int2);
   obj.disabled = true;
   document.getElementById("btn_cap1").disabled = true;
   document.getElementById("btn_cap2").disabled = true;
   var ta = document.getElementById("log_win");
   ta.value += "开始进行状态比对\n";
   ta.value += "\t-------------参照状态-----------\t";
   ta.value += "\t-------------当前状态-----------\n";
   xhr = new XMLHttpRequest();
   xhr.onreadystatechange=function(){
      if(xhr.readyState==4 && xhr.status==200){
         ta.value += xhr.responseText;
      }
   }
   var url = "ajax/ajax_check_state.php?ip=" + ip;
   xhr.open("GET",url,true);
   xhr.send();
   //
   var count = 5;
   int2 = setInterval(function(){
      if(count < 0){
         obj.value = '开始状态验证';
         document.getElementById("btn_cap1").disabled = false;
         document.getElementById("btn_cap2").disabled = false;
         document.getElementById("btn_mat").disabled = false;
      }else{
         obj.value = '正在比对' + count.toString();
      }
      count = count - 1;
   },1000);

}

