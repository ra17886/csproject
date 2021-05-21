var timeline =[]
var totalScore = 0
var r1 = 0
var r2= 0
var r3 = 0
var r4=0




  var info_sheet = {
    on_start: function(trial){
      document.querySelector('#jspsych-progressbar-container').style.display = 'none';
    },
    type: 'instructions',
    pages: [
        '<p style="font-weight:bold">Examining the effects of anxiety on reward-based decision-making using the Multi-Armed Bandit task</p><p>I would like to invite you to take part in my research project. Before you decide whether to participate or not, please read through the following information to gain an understanding of why the research is being conducted and what your participation will involve.</p> <p>Please get in contact if anything is unclear.</p><p>This research is being conducted as part of my final year MEng project. The purpose of the research is to compare the decision-making models of those suffering with anxiety and those who do not.<p> The research will be used to help gain a greater understanding of whether the current models that are used to study decision making are pertinent to those with heightened anxiety.</p>',
        '<p style="font-weight:bold">Am I eligible to participate?</p><p>You have been recruited from Prolific.co as the details you have entered match the eligibility criteria for the experiment.</p>'+
        '<p style="font-weight:bold">Do I have to take part?</p><p>It is up to you to decide whether you would like to participate in the study. You can withdraw at any time during the experiment by simply closing the tab; you do not have to give a reason for withdrawing. You cannot withdraw once the experiment is complete.</p><p>All information gathered during the experiment will be completely anonymised; your Prolific ID will not be stored and there is no other identifiable information. Data gathered from the experiment will be stored securely for the duration of the research project and may be made open in the future. All data published in my final report will be in summary form.</p>',
        '<p style="font-weight:bold">What will happen during the experiment?</p><p>The experiment will last approximately ten minutes and will start with a short survey. You will be asked to answer 28 questions about how you have been feeling during the last month. The questions are based on the Positive and Negative Affect Schedule (PANAS) and Patient Health Questionnaire 9 (PHQ-9).</p>'+
        '<p>The results of this survey will be used to identify any symptoms of depression and anxiety severity. These surveys will not be used to make a clinical diagnosis and we will be unable to contact you afterwards, even if the survery responses indicate symptoms of depression.</p>'+
        '<p>Please answer these questions openly and honestly.</p>',
        '<p style="font-weight:bold">What will happen during the experiment?</p><p>The second part of the experiment is a task designed to analyse your decision-making. The goal in this part of the experiment is to gain as many prizes as possible. In each trial you will be asked to choose between 4 boxes- each giving a different prize. The experiment will end when you have gained 20 prizes.</p><p>You will be given more detailed instructions on this task later in the experiment.</p>',
        '<p style="font-weight:bold">Will my participation in the project be kept confidential?</p>I will record your answers to the survey and your responses to the decision-making task; the boxes you chose during each trial and the prizes you gained. The data will be stored securely and kept strictly confidential. Your Prolific ID will be deleted; all data will be kept completely anonymised. If you choose to withdraw from the experiment, none of your data will be stored.',
        '<p style="font-weight:bold">What will happen to the results of the research project?</p><p>The results from the experiment will be included in the written thesis of my MEng project. The results will be presented in summary form and may be made open in the future.</p>'+
        '<p style="font-weight:bold">Who is organising and funding this research?</p><p>The research is part of my MEng undergraduate degree in Maths and Computer Science at the University of Bristol. It is funded by the Department of Computer Science and the James S McDonnell Foundation.</p>'+
        '<p style="font-weight:bold">Who has reviewed the study?</p><p>The study has been reviewed by the University of Bristol Faculty Research Ethics Committee Research Governance Team.</p>'
        +'<p style="font-weight:bold">Further Information and Contact Details</p><p>If you would like any further information about the study or if you have any questions, please contact me via email at ra17886@bristol.ac.uk. If you have any concerns regarding your participation in the study, please contact the Faculty of Ethics Research Governance Team, research-governance@bristol.ac.uk.</p>'
    ],
    show_clickable_nav: true
  }
  timeline.push(info_sheet)


  var consent_options=["Yes","No"]
  var consent_form_1 ={
    preamble:'Consent Form',
    type: 'survey-multi-choice',
    questions: [{prompt:"1. I have been given information explaining the study.",options:consent_options,required:true,horizonal:false},
    {prompt:"2. I have been given information about how my data will be used.",options:consent_options,required:true,horizonal:false},
    {prompt:"3. I am aware I can withdraw from the study during the experiment.",options:consent_options,required:true,horizonal:true}]
  }

  var consent_form_2 ={
    preamble:'Consent Form',
    type: 'survey-multi-choice',
    questions: [
    {prompt:"4. I am aware I cannot withdraw my data once the experiment is complete.",options:consent_options,required:true,horizonal:true},
    {prompt:"5. I have been given the opportunity to ask questions about the study.",options:consent_options,required:true,horizonal:true},
    {prompt:"6. I have recieved answers to any questions asked.",options:consent_options,required:true,horizonal:true}],
  }

  //loops through consent form until all answers are yes
  var loop_consent_form_1 ={
    timeline:[consent_form_1],
    loop_function: function(data){
      if(jsPsych.data.get().last(1).values()[0].responses.includes("No")){
        alert("If you wish to participate, you must be able to answer Yes to all questions")
        return true;
      }
      else return false;
    }
  }
  timeline.push(loop_consent_form_1);

  var loop_consent_form_2 ={
    timeline:[consent_form_2],
    loop_function: function(data){
      if(jsPsych.data.get().last(1).values()[0].responses.includes("No")){
        alert("If you wish to participate, you must be able to answer Yes to all questions")
        return true;
      }
      else return false;
    }
  }
  timeline.push(loop_consent_form_2);

 
  var prolific_id={
    type:'survey-text',
    questions:[{prompt:"What is your Prolific ID",required:true}],
  }
  timeline.push(prolific_id)

  var gender_options=["Male","Female","Non-Binary","Transgender","Intersex","Other","Prefer not to say"]
  var age_options=["18-25","25-34","35-44","45-54","55-64","65 or over"]
  var gender_age ={
    type:'survey-multi-choice',
    questions:[
      {prompt:"What is your gender?",options:gender_options,horizontal:false,required:true},
      {prompt:"Which age group describes you?", options:age_options,horizontal:false,required:true}
    ]
  };
  timeline.push(gender_age);

  var antidepressants={
    type:'survey-text',
    questions:[{prompt:"If you are currently taking an anti-depressant. Please enter which one in the box below."}]
  }
  timeline.push(antidepressants);

   
  var welcome_survey ={
    type:'instructions',
    pages: [
      'You will now be asked a series of questions about how you have been feeling over the past two weeks.<p>Please answer these questions open and honestly.</p>'
    ],
    show_clickable_nav: true
  }
  timeline.push(welcome_survey)
  
  var PANAS_scale = ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"];

  var PANAS_trial_1 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Indicate the extent you have felt this way over the past <u>2 weeks</u>.</p>',
      questions: [
        {prompt: "Interested", name: 'Interested', labels: PANAS_scale, required: true}, 
        {prompt: "Distressed", name: 'Distressed', labels: PANAS_scale, required: true}, 
        {prompt: "Excited", name: 'Excited', labels: PANAS_scale, required: true}, 
        {prompt: "Upset", name: 'Upset', labels: PANAS_scale, required: true}, 
      ]}

  var PANAS_trial_2 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Indicate the extent you have felt this way over the past <u>2 weeks</u>.</p>',
      questions: [
        {prompt: "Strong", name: 'Strong', labels: PANAS_scale, required: true}, 
        {prompt: "Guilty", name: 'Guilty', labels: PANAS_scale, required: true}, 
        {prompt: "Scared", name: 'Scared', labels: PANAS_scale, required: true}, 
        {prompt: "Hostile", name: 'Hostile', labels: PANAS_scale, required: true}, 
    ]}

  var PANAS_trial_3 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Indicate the extent you have felt this way over the past <u>2 weeks</u>.</p>',
      questions: [
        {prompt: "Enthusiastic", name: 'Enthusiastic', labels: PANAS_scale, required: true}, 
        {prompt: "Proud", name: 'Proud', labels: PANAS_scale, required: true}, 
        {prompt: "Irritable", name: 'Irritable', labels: PANAS_scale, required: true}, 
        {prompt: "Alert", name: 'Alert', labels: PANAS_scale, required: true}, 
    ]}

  var PANAS_trial_4 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Indicate the extent you have felt this way over the past <u>2 weeks</u>.</p>',
      questions: [
        {prompt: "Ashamed", name: 'Ashamed', labels: PANAS_scale, required: true}, 
        {prompt: "Inspired", name: 'Inspired', labels: PANAS_scale, required: true}, 
        {prompt: "Nervous", name: 'Nervous', labels: PANAS_scale, required: true}, 
        {prompt: "Determined", name: 'Determined', labels: PANAS_scale, required: true}, 
    ]}

  var PANAS_trial_5 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Indicate the extent you have felt this way over the past <u>2 weeks</u>.</p>',
      questions: [
        {prompt: "Attentive", name: 'Attentive', labels: PANAS_scale, required: true}, 
        {prompt: "Jittery", name: 'Jittery', labels: PANAS_scale, required: true}, 
        {prompt: "Active", name: 'Active', labels: PANAS_scale, required: true}, 
        {prompt: "Afraid", name: 'Afraid', labels: PANAS_scale, required: true}, 
         
      ]}
  timeline.push(PANAS_trial_1);
  timeline.push(PANAS_trial_2);
  timeline.push(PANAS_trial_3);
  timeline.push(PANAS_trial_4);
  timeline.push(PANAS_trial_5);

  var PHQ_scale = ["Not at all", "Several days","More than half the days","Nearly every day"];

  var PHQ_trial_1 = {
      type: 'survey-likert',
      preamble:'<p style="color:red">Over the last <u>2 weeks</u>, how often have you been bothered by any of the following problems?</p>',
      questions: [
        {prompt: "Little interest or pleasure in doing things", labels: PHQ_scale, required: true}, 
        {prompt: "Feeling down, depressed, or hopeless", labels: PHQ_scale, required: true}, 
        {prompt: "Trouble falling or staying asleep, or sleeping too much", labels: PHQ_scale, required: true}, 
        {prompt: "Feeling tired or having little energy", labels: PHQ_scale, required: true}, 
       
      ],
      scale_width:750,
  };
  timeline.push(PHQ_trial_1);

  var PHQ_trial_2 = {
    type: 'survey-likert',
    preamble: '<p style="color:red">Over the last <u>2 weeks</u>, how often have you been bothered by any of the following problems?</p>',
    questions: [
      {prompt: "Poor appetite or overeating", labels: PHQ_scale, required: true}, 
  {prompt: "Feeling bad about yourself - or that you are a failure or have let yourself or your family down", labels: PHQ_scale, required: true}, 
  {prompt: "Trouble concentrating on things, such as reading the newspaper or watching television", labels: PHQ_scale, required: true}, 
  {prompt: "Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual", labels: PHQ_scale, required: true},
    ],
    scale_width:750,
  };
  timeline.push(PHQ_trial_2);

   

  var GAD7_scale = ["Not at all", "Several days","More than half the days","Nearly every day"];

  var GAD7_trial_1 = {
      type: 'survey-likert',
      preamble: '<p style="color:red">Over the last <u>2 weeks</u>, how often have you been bothered by any of the following problems?</p>',
      questions: [
        {prompt: "Feeling nervous, anxious or on edge", labels: GAD7_scale, required: true}, 
        {prompt: "Not being able to stop or control worrying", labels: GAD7_scale, required: true}, 
        {prompt: "Worrying too much about different things", labels: GAD7_scale, required: true}, 
        {prompt: "Trouble relaxing", labels: GAD7_scale, required: true}, 
        
      ],
  };
  timeline.push(GAD7_trial_1); 

  var GAD7_trial_2 = {
    type: 'survey-likert',
    preamble: '<p style="color:red">Over the last <u>2 weeks</u>, how often have you been bothered by any of the following problems?</p>',
    questions: [
      {prompt: "Being so restless that it is hard to sit still", labels: GAD7_scale, required: true}, 
      {prompt: "Becoming easily annoyed or irritable", labels: GAD7_scale, required: true}, 
      {prompt: "Feeling afraid as if something bad might happen", labels: GAD7_scale, required: true}, 
      
    ],
};
timeline.push(GAD7_trial_2); 

  

  
var experiment_instructions = {
  type: 'instructions',
  on_start: function(trial){
    totalScore =0;
    updateProgress();
    document.querySelector('#jspsych-progressbar-container').style.display = 'block';
    generateRewardRates();
  },
  pages: [
      'Welcome to the second part of the experiment. Here, you will complete a short decision-making task.',
      '<p>At each stage, you will be presented with 4 present boxes; some will contain prizes but some will be empty.</p><p> Each coloured box gives prizes at a different rate.</p><p> <img src="img/boxes/blueclosedbox.png" width="15%"><img> <img src="img/boxes/greenclosedbox.png" width="15%"><img></p>' +'<p> <img src="img/boxes/purpleclosedbox.png" width="15%"><img> <img src="img/boxes/redclosedbox.png" width="15%"><img></p>',
      '<p>The experiment will end when you have gained 20 prizes.</p><p>You will first complete a short practise trial of 3 rounds. None of the decisions you make during the next section will be analysed. <p>Please press next to continue to the practise round.</p>'
  ],
  show_clickable_nav: true
}
timeline.push(experiment_instructions)

  function correctDistance(a,b){
    return a-b>0.1
  }

  function correctDistances(a,b,c,d){
    return correctDistance(a,b) && correctDistance(a,c) && correctDistance(a,d) && correctDistance(b,c) && correctDistance(b,d) && correctDistance(c,d)
  }

  function generateRewardRates(){
    var r = [0,0,0,0]
    for(i=0;i<r.length;i++){
      r[i]= jStat.beta.sample( 2, 2 );
    }
      while(!correctDistances(r[0],r[1],r[2],r[3])){
        for(i=0;i<r.length;i++){
          r[i]= jStat.beta.sample( 2, 2 );
        }
      }
        var random = Math.floor(Math.random() * r.length);
        r1 = r.splice(random, 1)[0];

        var random = Math.floor(Math.random() * r.length);
        r2 = r.splice(random, 1)[0];

        var random = Math.floor(Math.random() * r.length);
        r3 = r.splice(random, 1)[0];

        var random = Math.floor(Math.random() * r.length);
        r4 = r.splice(random, 1)[0];
  }

  function resetRewardRates(){
    r1 = 0;
    r2=0;
    r3=0;
    r4=0;
  }

  //then add trial, display 4 boxes and the user selects one with mouse or keyboard
  var test ={
    type: 'html-button-response',
    stimulus: '<p>Choose a box,</p>',
    choices:['1','2','3','4'],
    button_html: ['<button><img src=img/boxes/blueclosedbox.png></img></button>','<button><img src=img/boxes/greenclosedbox.png></img></button>','<button><img src=img/boxes/purpleclosedbox.png></img></button>','<button><img src=img/boxes/redclosedbox.png></img></button>'],
    
  };

  function calculateValue(arm){

    var rewardRate;
    if(arm==0) rewardRate = r1;
    if(arm==1) rewardRate =r2;
    if(arm==2) rewardRate =r3;
    if(arm==3) rewardRate =r4;

    var num = Math.random();

    if(num < rewardRate) return 1;
    else return 0;
  };

  function updateProgress(){
    jsPsych.setProgressBar(totalScore/20);
    document.querySelector("#jspsych-progressbar-container > span").innerText = totalScore+"/20";
  }

  function generatePunishment(chosen_arm){
    var image;
    if (chosen_arm==0) image='blue'
    if(chosen_arm==1) image='green'
    if(chosen_arm==2) image='purple'
    if(chosen_arm==3) image ='red'

    var feedback = '<div style="background-color:#ff7157"><h1 style="background-color:Tomato">Bad luck! There was no prize in the box!</h1>'+
    '<h1 style="background-color:Tomato">Remember, you need to keep going until you have 20 prizes!</h1>'+'<img id="box" src="img/sad/' + image+ 'openboxsadthumb.png"></img></div>'
    return feedback
  }

  function generateReward(chosen_arm){
    var prizes = new Array();
    prizes[0]='beachball'
    prizes[1] = 'bear'
    prizes[2]='choc'
    prizes[3]='coins'
    prizes[4]='duck'
    prizes[5]='flowers'
    prizes[6]='lolipop'
    prizes[7]='ring'
    prizes[8]='yoyo'

    var image;
    if (chosen_arm==0) image='blue'
    if(chosen_arm==1) image='green'
    if(chosen_arm==2) image='purple'
    if(chosen_arm==3) image ='red'

    var number = Math.floor(Math.random()*prizes.length);
    prize = prizes[number]

    var feedback = '<div style="background-color:#6dce98"><h1 style="background-color:MediumSeaGreen" >You won a prize! Well done!</h1>' +'<div style="background-color:#6dce98"><h1 style="background-color:MediumSeaGreen" >Only '+ (20-totalScore) +' left to go!</h1>'+ '<img id="box" src="img/prizes/' + prize+ '.png"></img>' + '<img id="box" src="img/empty/' + image+ 'openbox.png"></img></div>'
    return feedback
  }



  function generateFeedback(chosen_arm){
    var value = calculateValue(chosen_arm)
    var feedback
    totalScore = totalScore + value
    updateProgress();
    var display_arm = chosen_arm +1
    if(value == 0) feedback = generatePunishment(chosen_arm)
    if(value ==1) feedback = generateReward(chosen_arm)
   // return "<p>You chose arm</p>" + display_arm + "<p>You scored </p>" + value + "<p>Your current total is" + totalScore
    return feedback
  }

  var feedback={
    type: 'html-keyboard-response',
    stimulus: function(){
    var arm = jsPsych.data.get().last(1).values()[0].button_pressed
    var rewardRate;
    if(arm==0) rewardRate = r1;
    if(arm==1) rewardRate =r2;
    if(arm==2) rewardRate =r3;
    if(arm==3) rewardRate =r4;


    jsPsych.data.write({rate: rewardRate});

    return generateFeedback(arm)
    },
   choices: jsPsych.NO_KEYS,
   trial_duration:1500
  }


  var practise_procedure = {
    on_start: function(trial){
      document.querySelector('#jspsych-progressbar-container').style.display = 'block';
    },
    timeline: [test, feedback],
    repetitions: 3,
    on_finish: function(trial){
      document.querySelector('#jspsych-progressbar-container').style.display = 'none';
    }
  }
  timeline.push(practise_procedure);

  var exp_start ={
    type:'instructions',
    on_start: function(trial){
      totalScore =0;
      updateProgress();
      document.querySelector('#jspsych-progressbar-container').style.display = 'block';
      generateRewardRates();
    },
    pages: [
      'The experiment will begin now. Please note, the rate at which boxes give prizes has been reset and will be different to the previous trial.<p>The experiment will end when you have gained 20 prizes.</p>'
    ],
    show_clickable_nav: true
  }
  timeline.push(exp_start)

  var experiment_loop={
    timeline:[test,feedback],
    loop_function: function(data){
      return (totalScore<20)
  }
}
timeline.push(experiment_loop);

var final_questions={
  type:'survey-text',
  preamble: "Please answer the following questions",
  questions:[{prompt:"What did you think of this experiment?",rows:3},{prompt:"What strategy did you use to choose boxes?",rows:3}],
}
timeline.push(final_questions)

function saveData(filename, filedata){
  $.ajax({
     type:'post',
     cache: false,
     url: 'save_data.php',
     data: {filename: filename, filedata: filedata},
     success: function(){
      window.location.assign("finish.html");
     }
  });
}

  

  jsPsych.init({
    timeline: timeline,
    show_progress_bar: true,
    override_safe_mode: true,
    auto_update_progress_bar:false,
    message_progress_bar: totalScore+"/20",
    on_finish: function(data) {
     
     
     saveData("mab",jsPsych.data.get().json());
     //window.location.assign("finish.html");


   
     
     resetRewardRates();
   }
  }
  );