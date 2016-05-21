<?php
  require_once '../function/fun.php';
  require_once '../function/class.phpmailer.php';
  require_once '../function/class.smtp.php';
  
  session_start();
  if(isset($_SESSION['user']) && $_SESSION['user']=='admin'){
     $server = $_GET['server'];
     $usr = $_GET['usr'];
     $pwd = $_GET['pwd'];
     $rev = $_GET['rev'];

     $mail = new PHPMailer;
     $mail->isSMTP();                  // Set mailer to use SMTP
     $mail->Host = $server;            // Specify main and backup SMTP servers
     $mail->SMTPAuth = true;
     $mail->Username = $usr;
     $mail->Password = $pwd;
     $mail->Subject = '来自netmon测试邮件';
     $mail->Body    = '这是测试正文 <b>in bold!</b>';
     $mail->CharSet = 'utf-8';

     $mail->setFrom($usr);
     $mail->addAddress($rev);

     if(!$mail->send()) {
        $msg = "admin发送测试邮件失败\n";
        $msg = $msg . 'Mailer Error: ' . $mail->ErrorInfo;
        $logger->warn($msg);
        echo $msg;
     } else {
        $msg = 'admin发送测试邮件成功';
        $logger->info($msg);
        echo $msg;
     }
     return;
  }else{
     echo "请先登录";
  }
?>
