<?php
include 'class.logger.php';
$file = __DIR__. '/../log/web.log';
$logger = new Logger('web', $file);
$logger->setLogLevel(20);
?>
