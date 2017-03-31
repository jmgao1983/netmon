<?php
include 'header.php';
//判断是否登录用户
if(isset($_SESSION['user'])){
   if($_SESSION['user'] == 'admin'){
      $mysql = "select corp,rname,rip from router where app>=2";
   }else{
      $mysql = "select corp,rname,rip from router where app>=2 and city='". $_SESSION['city']. "'";
   }
   $mysql = $mysql . " order by rname";
   //获取当前分页页面和每页显示行数
   $rnum = isset($_GET['rnum']) ? $_GET['rnum'] : 15;
   $page = isset($_GET['page']) ? $_GET['page'] : 1;
   $count = ($page - 1) * $rnum;
   $sql = $mysql." limit $count,$rnum";

   //获取主表当前页显示内容
   $target = xget($sql);
   //var_dump($target);
   //获取所有条目的数目
   $all = xget($mysql);
   $total = count($all);   //
?>

<div class = 'device'>
   <table id = "display">
      <tr>
        <td><input type="text" size="6" value="厂商" readonly></td>
        <td><input type="text" size="15" value="名称" readonly></td>
        <td><input type="text" size="15" value="地址" readonly></td>
        <td><input type="text" size="8" value="操作" readonly></td>
      </tr>
      <?php //显示设备表?>
      <?php for($i=0; $i<count($target); $i++){ ?>
      <tr>
        <td><span><?php echo $target[$i]['corp']; ?></span></td>
        <td><span><?php echo $target[$i]['rname']; ?></span></td>
        <td><span><?php echo $target[$i]['rip']; ?></span></td>
        <td><select onchange=operate(this,'<?php echo $target[$i]['rip'] ?>')>
               <option><p>请选择</p></option>
               <option><p>测试登陆</p></option>
               <option><p>保存配置</p></option>
               <option><p>验证状态</p></option>
               <option><p>删除设备</p></option>
            </select>
        </td>
      </tr>
      <?php } ?>
   </table>
   <?php //分页功能?>
   <div id="pagenav">
      <?php for($a=5; $a>0; $a--){?>
         <a href="tool.php?page=<?php echo $page-$a;?>&rnum=<?php echo $rnum ?>">
            <?php if($page-$a>0){echo $page-$a;}?></a>
      <?php }?>

      <strong><?php echo $page; ?></strong>

      <?php for($b=1; $b<=5; $b++){ ?>
         <a href="tool.php?page=<?php echo $b+$page;?>&rnum=<?php echo $rnum ?>">
            <?php if($b+$page<=(int)($total/$rnum)+1)echo $page+$b;?></a>
      <?php }?>
      <span>当前<strong><?php echo $total ?></strong>个设备</span>
      <span id="page_info">[每周日凌晨自动保存配置]</span>
   </div>
   
   <br/><strong>添加设备</strong><br/>
   <select id = "s_vendor">
      <option value='-1'>选择厂商</option>
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
   <select id = "s_proto">
      <option value='-1'>协议</option>
      <option value='22'>ssh</option>
      <option value='23'>telnet</option>
   </select>
   <select id = "s_auth" onchange=input_pass(this)>
      <option value='-1'>登陆方式</option>
      <option value='0'>用户|密码1|密码2</option>
      <option value='1'>密码1|密码2|</option>
      <option value='2'>用户|密码|</option>
   </select>
   <p id = "pass"></p>
   <p>
     <button onclick=add_device(this)>确定</button>&nbsp;
     <span id="txt_out"></span>
   </p>

</div>

<?php }else{ ?>
<div class='device'>
  <h3>请先登录</h3>
</div>
<?php
}
include 'footer.php';
?>

