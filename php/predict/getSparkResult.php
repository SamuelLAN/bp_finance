<?php

if(!isset($_COOKIE['username'])) {
    echo 0;
    exit;
}
$unique_id = $_COOKIE['username'];

$tmp_path = '../../tmp/' . $unique_id;

$path = $tmp_path . '/bestAccuracyResult.tmp';
$best_accuracy_content = @file_get_contents($path);

$path = $tmp_path . '/bestDiffResult.tmp';
$best_diff_content = @file_get_contents($path);

$path = $tmp_path . '/bestCostResult.tmp';
$best_cost_content = @file_get_contents($path);

$path = $tmp_path . '/bestValidationAccuracyResult.tmp';
$best_validation_accuracy_content = @file_get_contents($path);

$path = $tmp_path . '/bestRelativeCostResult.tmp';
$best_relative_cost_content = @file_get_contents($path);

echo json_encode(array(
    'best_accuracy' => $best_accuracy_content,
    'best_diff' => $best_diff_content,
    'best_cost' => $best_cost_content,
    'best_validation_accuracy' => $best_validation_accuracy_content,
    'best_relative_cost' => $best_relative_cost_content,
));
