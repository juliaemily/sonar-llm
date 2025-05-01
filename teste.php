<?php
$input = $_GET['x'];
eval($input); // alerta clássico de vulnerabilidade
