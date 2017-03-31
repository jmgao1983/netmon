<?php
include 'header-admin.php';
require_once 'function/fun.php';
if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
   $sql = "select city from city where id>1 order by id";
   $cities = xget($sql);
  
   //// 设备管理相关数据
   $mysql = "select corp,rname,rip,city from router where app=3";
   //获取设备当前分页页面和每页显示行数
   $router_rnum = isset($_GET['router_rnum']) ? $_GET['router_rnum'] : 5;
   $router_page = isset($_GET['router_page']) ? $_GET['router_page'] : 1;
   $router_pos = ($router_page - 1) * $router_rnum;
   $sql = $mysql." limit $router_pos,$router_rnum";
   //获取设备表当前页显示内容
   $router = xget($sql);
   //获取设备表所有条目的数目
   $all = xget($mysql);
   $router_total = count($all);
   
   //// 用户管理相关数据
   $mysql = "select name,city from user where name!='admin'";
   //获取用户表当前分页页面和每页显示行数
   $user_rnum = isset($_GET['user_rnum']) ? $_GET['user_rnum'] : 5;
   $user_page = isset($_GET['user_page']) ? $_GET['user_page'] : 1;
   $user_pos = ($user_page - 1) * $user_rnum;
   $sql = $mysql." limit $user_pos,$user_rnum";
   //获取用户表当前页显示内容
   $user = xget($sql);
   //获取用户表所有条目的数目
   $all = xget($mysql);
   $user_total = count($all);

?>
<div class = "main">
  <!------------------------------------------------>
  <h5>城市管理</h5>
  <div class="panel">
     <?php for($i=0; $i<count($cities); $i++){ ?>
        <a href="" onclick="ajax_del_city('<?php echo $cities[$i]['city']?>');return false;">
           <?php echo $cities[$i]['city']?>
        </a>&nbsp;
     <?php } ?>
     <button onclick=ajax_add_city()>添加</button>
  </div>
  <!------------------------------------------------>
  <h5>设备管理</h5>
  <div class="panel">
     <select id = "s_vendor">
       <option value='-1'>厂商</option>
       <option value='01'>cisco</option>
       <option value='02'>h3c</option>
       <option value='03'>huawei</option>
       <option value='04'>ruijie</option>
       <option value='05'>junos</option>
       <option value='06'>dell</option>
       <option value='99'>...</option>
     </select>
     <input type="text" id="txt_dname" size="10" value="设备名称">
     <input type="text" id="txt_ip" size="10" value="设备IP">
     <select id ="s_city">
       <option>城市</option>
       <?php for($i=0; $i<count($cities); $i++){ ?>
          <option><?php echo $cities[$i]['city']?></option>
       <?php } ?>
     </select>
     <select id = "s_proto">
       <option value='-1'>协议</option>
       <option value='22'>ssh</option>
       <option value='23'>telnet</option>
     </select>
     <select id = "s_auth" onchange=input_pass(this)>
       <option value='-1'>登陆方式</option>
       <option value='0'>用户|密码1|密码2</option>
       <option value='1'>密码1|密码2</option>
       <option value='2'>用户|密码</option>
     </select>
     <button onclick=ajax_add_router(this)>添加</button>&nbsp;
     <span id="txt_out" class="txt_warn"></span>
     <div id="pass"></div>

     <table id = "display"><?php //显示设备表?>
      <?php for($i=0; $i<count($router); $i++){ ?>
      <tr>
        <td><span><?php echo $router[$i]['corp']; ?></span></td>
        <td><span><?php echo $router[$i]['rname']; ?></span></td>
        <td><span><?php echo $router[$i]['rip']; ?></span></td>
        <td><span><?php echo $router[$i]['city']; ?></span></td>
        <td><a class="oper" href=""
             onclick="ajax_del_router('<?php echo $router[$i]['rip'] ?>');return false;" >删除</a>
        </td>
      </tr>
      <?php } ?>
     </table>
     <?php //分页功能?>
     <div id="pagenav">
       <?php for($a=5; $a>0; $a--){?>
         <a href="admin.php?router_page=<?php echo $router_page-$a;?>&router_rnum=<?php echo $router_rnum ?>">
            <?php if($router_page-$a>0){echo $router_page-$a;}?></a>
       <?php }?>

       <strong><?php echo $router_page; ?></strong>

       <?php for($b=1; $b<=5; $b++){ ?>
         <a href="admin.php?router_page=<?php echo $b+$router_page;?>&router_rnum=<?php echo $router_rnum ?>">
            <?php if($b+$router_page<=(int)($router_total/$router_rnum)+1)echo $router_page+$b;?></a>
       <?php }?>
       <span>当前<strong><?php echo $router_total ?></strong>个设备</span>
     </div>
  </div>
  <!------------------------------------------------>
  <h5>用户管理</h5>
  <div class="panel">
     <select id ="s_city2">
       <option>城市</option>
       <?php for($i=0; $i<count($cities); $i++){ ?>
          <option><?php echo $cities[$i]['city']?></option>
       <?php } ?>
     </select>
     用户
     <input type="text" id="add_user" size="10">
     密码
     <input type="password" id="add_pwd1" size="10">
     确认
     <input type="password" id="add_pwd2" size="10">
     <button onclick=ajax_add_user()>添加</button>
     <span id="user_output" class="txt_warn"></span>
     
     <table id = "display"><?php //显示用户表?>
      <?php for($i=0; $i<count($user); $i++){ ?>
      <tr>
        <td><span><?php echo $user[$i]['city']; ?></span></td>
        <td><span><?php echo $user[$i]['name']; ?></span></td>
        <td><a class="oper" href=""
             onclick="ajax_del_user('<?php echo $user[$i]['name'] ?>');return false;" >删除</a>
        </td>
      </tr>
      <?php } ?>
     </table>
     <?php //分页功能?>
     <div id="pagenav">
       <?php for($a=5; $a>0; $a--){?>
         <a href="admin.php?user_page=<?php echo $user_page-$a;?>&user_rnum=<?php echo $user_rnum ?>">
            <?php if($user_page-$a>0){echo $user_page-$a;}?></a>
       <?php }?>

       <strong><?php echo $user_page; ?></strong>

       <?php for($b=1; $b<=5; $b++){ ?>
         <a href="admin.php?user_page=<?php echo $b+$user_page;?>&user_rnum=<?php echo $user_rnum ?>">
            <?php if($b+$user_page<=(int)($user_total/$user_rnum)+1)echo $user_page+$b;?></a>
       <?php }?>
       <span>当前<strong><?php echo $user_total ?></strong>个用户</span>
     </div>
  </div>

</div>
<?php }else{ ?>
<div class='down'>
  <h3>请以管理员登录</h3>
</div>
<?php
}
include 'footer.php';
?>
