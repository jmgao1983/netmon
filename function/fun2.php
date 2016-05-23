<?php
   function my_encode($str, $seed){
      $tmp = md5($seed);
      $N = strlen($str);
      $offset = 0;
      $re = '';
      for($i = 0; $i < $N; $i++){
         $offset = ord($tmp[$i]) > 96 ? (ord($tmp[$i])-87) : (ord($tmp[$i])-48);
         $re = $re. chr(ord($str[$i]) - $offset);
      }
      //因为数据库存储时也会对字符进行转义; 为使密码保持原样存储，使用addslashes()
      //在某些字符前加上反斜线。单引号（'）、双引号（"）、反斜线（\）与 NUL（ NULL 字符）
      return addslashes($re);
      //return $re;
   }

   function my_decode($str, $seed){
      $tmp = md5($seed);
      $N = strlen($str);
      $offset = 0;
      $re = '';
      for($i = 0; $i < $N; $i++){
         $offset = ord($tmp[$i]) > 96 ? (ord($tmp[$i])-87) : (ord($tmp[$i])-48);
         $re = $re. chr(ord($str[$i]) + $offset);
      }
      return $re;
   }
   
   //$test = '!"#$%&()*+,-./:;<=?@[\]^-`{}|~';
   //$test = 'ccbwlgl0701';
   //echo $test;
   //echo "\n";
   //echo my_encode($test,'ZJ_TZ_ECN_SW_1');
   //echo "\n";
   //echo my_decode(my_encode($test,'ZJ_TZ_ECN_SW_1'),'ZJ_TZ_ECN_SW_1');
   //echo "\n";
?>
