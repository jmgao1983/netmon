<?php
include 'header-index.php';

//################第一部分数据查询
//获取用户所在城市
$city = get_city();
if($city == '全部'){
   $mysql = "select * from target where pri<5 ";
   $sql_rname = "select rname from router order by rname";
}else{
   $mysql = "select * from target where city='". $city. "' ";
   $sql_rname = "select rname from router where city='". $city. "' order by rname";
}
//var_dump($mysql);

//筛选条件判断与COOKIE设置
$mysql = get_filter($mysql);
//var_dump($mysql);

//获取当前分页页面和每页显示行数
$rnum = isset($_GET['rnum']) ? $_GET['rnum'] : 20;
$page = isset($_GET['page']) ? $_GET['page'] : 1;
$count = ($page - 1) * $rnum;
$sql = $mysql." limit $count,$rnum";

//获取主表当前页显示内容
$target = xget($sql);
//获取所有条目的数目
$all = xget($mysql);
$total = count($all);

//获取'接入点'下拉框中的设备列表
$s_rname = xget($sql_rname);
?>

<?php //第二部分主表显示 ?>

<div class = "main">
   <table id = "display">
      <tr>  </tr>
      <tr id = "filter">
	 <td><select id="rname" onchange=filter()>
	       <option value='-1'>接入设备</option>
       <?php for($i=0; $i<count($s_rname); $i++){ ?>
          <option value=<?php echo $s_rname[$i]['rname'];?>>
             <?php echo $s_rname[$i]['rname'];?>
          </option>
       <?php } ?>
	    </select></td>
	 <td><input type="text" id="tdes" size="20" value="单位名称" onchange=filter()></td>
	 <td><input type="text" id="tip" size="16" value="互联地址" onchange=filter()></td>
	 <td><select id="isp" onchange=filter()>
	       <option value='-1'>运行商</option>
	       <option value='DX'>电信</option>
	       <option value='LT'>联通</option>
	       <option value='HS'>华数</option>
	       <option value='YD'>移动</option>
	       <option value='QT'>其他</option>
	    </select></td>
	 <td><select id="rtt" onchange=filter()>
	       <option value='-1'>线路状态</option>
	       <option value='Up'>通</option>
	       <option value='Down'>断</option>
	    </select></td>
	 <td>
	    <button onclick=clear_filter()>清除条件</button>
	  </td>
      </tr>
      <?php for($i=0; $i<count($target); $i++){ ?>
      <tr>
	 <td><span><?php echo $target[$i]['rname']; ?></span></td>
	 <td><span><?php echo $target[$i]['tdes']; ?></span></td>
	 <td><span><?php echo $target[$i]['tip']; ?></span></td>
	 <td><span><?php echo $target[$i]['isp']; ?></span></td>
	 <?php if($target[$i]['pri']==0){ ?>
       <td><span class="disabled">disabled</span></td>
    <?php }else{ ?>
	    <?php if($target[$i]['rtt']==0){ ?>
	       <td><span class="down">down</span></td>
	    <?php }else{ ?>
	       <td><span class="up"><?php echo $target[$i]['rtt']."ms"; ?></span></td>
	    <?php }?>
    <?php }?>
	 <td>
	  <?php if(isset($_SESSION['user'])){?>
	    <!-- 使用ajax删除功能和非ajax修改功能 -->
	    <a class="oper" name="<?php echo $target[$i]['tdes'] ?>"
	      href="" onclick="ajax_rm_target(this);return false;" >删除</a>
	    <a class="oper" href="RecordUpdate.php?tdes=<?php 
	      echo $target[$i]['tdes'] ?>&tip=<?php 
	      echo $target[$i]['tip'] ?>">编辑</a>
	    <a class="oper" href="" onclick=
	      "ajax_det_target(<?php echo "'".$target[$i]['tdes']."'";?>);return false;" >详情</a>
	  <?php } ?>
	 </td>
      </tr>
      <?php } ?>
   </table>

<?php //第三部分 分页功能?>

   <div id="pagenav">
      <select id="rowNumber" onchange=change_row_number()>
	<option value='0'>每页行数</option>
	<option value='10'>每页10行</option>
	<option value='30'>每页30行</option>
	<option value='50'>每页50行</option>
	<option value='100'>每页100行</option>
	<option value='200'>每页200行</option>
      </select>

      <?php for($a=5; $a>0; $a--){?>
         <a href="index.php?page=<?php echo $page-$a;?>&rnum=<?php echo $rnum ?>">
	    <?php if($page-$a>0){echo $page-$a;}?></a>
      <?php }?>

      <strong><?php echo $page; ?></strong>

      <?php for($b=1; $b<=5; $b++){ ?>
	 <a href="index.php?page=<?php echo $b+$page;?>&rnum=<?php echo $rnum ?>">
	    <?php if($b+$page<=(int)($total/$rnum)+1)echo $page+$b;?></a>
      <?php }?>
      <span>总共<strong><?php echo $total ?></strong>个结果</span>

      <?php if(isset($_SESSION['user'])){?>
	<!--按钮的onclick事件控制[增加]功能-->
	<button onclick="add_show()">增加</button>
      <?php } ?>
   </div>

<?php //第四部分 使用ajax增加记录 ?>

  <div id="rec_add">  
	 <select id="rname_add">
	    <option value='-1'>接入设备</option>
       <?php for($i=0; $i<count($s_rname); $i++){ ?>
       <option value=<?php echo $s_rname[$i]['rname'];?>>
          <?php echo $s_rname[$i]['rname'];?>
       </option>
       <?php } ?>
	 </select>
    <input type="text" id="tdes_add" size="10" value="单位名称">
    <input type="text" id="tip_add" size="10" value="互联IP">
    <select id="isp_add">
      <option value='-1'>运行商</option>
      <option value='DX'>电信</option>
      <option value='LT'>联通</option>
      <option value='HS'>华数</option>
      <option value='YD'>移动</option>
      <option value='QT'>其他</option>
    </select>
    <button id="add_confirm" onclick=ajax_add_target()>确定</button>
    <span id="result"></span>
  </div>

</div>

<?php
include 'footer.php';
?>
