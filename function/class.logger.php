<?php
/*
 * PHP Logger Class
 */

define('LEVEL_FATAL', 50);
define('LEVEL_ERROR', 40);
define('LEVEL_WARN', 30);
define('LEVEL_INFO', 20);
define('LEVEL_DEBUG', 10);


class Logger {

    static $LOG_LEVELS = array('NOSET', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL');

    private $name  = 'root';
    private $level = LEVEL_DEBUG;
    private $file  = './root.log';

    function __construct($name = 'root', $file = './root.log', $lvl = 4) {
       $this->name = $name;
       $this->file = $file;
    }

    function setLogLevel($lvl) {
        if($lvl > 50  || $lvl < 10) {
            throw new Exception('invalid log level:' . $lvl);
        }
        $this->level = $lvl;
    }

    function file_force_contents($filename, $data, $flags = 0){
       if(!is_dir(dirname($filename)))
           mkdir(dirname($filename).'/', 0777, TRUE);
       return file_put_contents($filename, $data,$flags);
    }

    function _log($level, $message) {
        if($level < $this->level) {
            return;
        }
    
        $log_level_name = Logger::$LOG_LEVELS[$level/10];
        $content = date('Y-m-d H:i:s') . ' [' . $this->name . '] ' .$log_level_name . " ". $message . "\n";
        $this->file_force_contents($this->file, $content, FILE_APPEND);
    }


    function debug($message) {
        $this->_log(LEVEL_DEBUG, $message);
    }
    function info($message) {
        $this->_log(LEVEL_INFO, $message);
    }
    function warn($message) {
        $this->_log(LEVEL_WARN, $message);
    }
    function error($message) {
        $this->_log(LEVEL_ERROR, $message);
    }
    function fatal($message) {
        $this->_log(LEVEL_FATAL, $message);
    }
}

//
