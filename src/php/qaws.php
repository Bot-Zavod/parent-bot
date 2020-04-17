<?php
$token = "";

function sendMessage($chat_id, $text){
	global $token;
	$url = "https://api.telegram.org/bot".$token."/sendMessage?chat_id=".$chat_id."&text=".$text."&parse_mode=markdown";
	$res = file_get_contents($url);
	return $res;
}
function sendSticker($chat_id, $sticker){
	global $token;
	$url = "https://api.telegram.org/bot".$token."/sendSticker?chat_id=".$chat_id."&sticker=".$sticker;
	$res = file_get_contents($url);
	return $res;
}
function deleteMessage($chat_id, $message_id){
	global $token;
	$url = "https://api.telegram.org/bot".$token."/deleteMessage?chat_id=".$chat_id."&message_id=".$message_id;
	$res = file_get_contents($url);
	return $res;
}

// ////////////////////////////////////////////////////////////////
$file = fopen("qalog.log", 'a');
$res = var_export($_POST, true); 
$signature = base64_decode($_POST['signature']);
$data = base64_decode($_POST['data']);

fwrite($file, "\n\n========".date("Y-m-d h:i:sa")."========");
fwrite($file, "\nRAW data: " . $res); 
fwrite($file, "\nsignature: " . $signature);
fwrite($file, "\ndata: " . $data);
fwrite($file, "\n=====================================");
// ////////////////////////////////////////////////////////////////

// Нужно не отправлять сообщение, а заменять сообщение с предложением подписки!!!!!!!
$json_data = json_decode($data);

$payment_id = $json_data->payment_id;
$status = $json_data->status;
$description = explode(":", $json_data->description);
$chat_id = $description[1];
$message_id = $description[2];

$text = "*Подписка №".$payment_id." оформлена. Напишите команду /start!*";
$sticker = "CAACAgIAAxkBAAEEVE5emCZWZkG0WeejU9oIEgmR-RdwygACFQADwDZPE81WpjthnmTnGAQ";

try{
  $delete = deleteMessage($chat_id, $message_id);
  $stiker = sendSticker($chat_id, $sticker);
  $content = sendMessage($chat_id, $text);

}  catch (Exception $e) { 
  fwrite($file, "\nERROR: " . $e);
};

fclose($file);


// $db = new SQLite3('parent.sql');
// var_dump($db->query('SELECT * FROM Users'));