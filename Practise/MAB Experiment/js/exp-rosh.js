var instruction_block ={
    type: 'html',
    stimulus: "Welcome to the experiment"
}


var experiment_blocks =[
    instruction_block
];

jsPsych.init({
    timeline: experiment_blocks,
   // on_finish: function() {
   //   jsPsych.data.displayData();
   // }
});