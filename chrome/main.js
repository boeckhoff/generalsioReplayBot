function remove(){
try
  {
    document.getElementById('replay-top-left').innerHTML = '';
  }
catch(err)
  {
  }
  try
  {
        document.getElementById('turn-counter').innerHTML = '';
        document.getElementById('turn-counter').style.visibility = "hidden";
  }
catch(err)
  {
  }
  try
  {
        document.getElementById('share-replay-button').innerHTML = '';
  }
catch(err)
  {
  }
  try
  {
        document.getElementById('replay-bottom').innerHTML = '';
  }
catch(err)
  {
  }
document.getElementsByClassName("relative")[0].style.top = 0
document.getElementsByClassName("relative")[0].style.left = 0
}
setTimeout(function(){remove();},2000);
remove();
