function dip()
        {
            var check=document.getElementById('diploma');

            if(check.checked){
            document.getElementById("sem1").style.display = 'none';
            document.getElementById('sem2').style.display='none';
            document.getElementById("diplo").style.display = '';
            document.getElementById("hsc").style.display = 'none';
            }
            else{
                document.getElementById("sem1").style.display = '';
                document.getElementById('sem2').style.display='';
                document.getElementById('diplo').style.display='none';
                document.getElementById("hsc").style.display = '';
            }
        }