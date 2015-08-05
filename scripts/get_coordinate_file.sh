#Created by zjshao 2014-7-10
#Modified by zjshao 2015-7-30 
#Create .xyz file for specified step

step=$1  # get the step number
step_size=$(echo $step | wc -L)  # get the length of step
space_size=$[9-$step_size]

#get the number line of the step 
line_num=$(sed -n '/^STEP =\s\{'$space_size'\}'$step'$/=' OUT.ANI)

#get the number of lines this step has
natoms=$(sed -n '7p' POSCAR | awk '{sum=0;for(i=1;i<=NF;i++)sum+=$i;print sum}')
startline=$(expr $line_num - 1)
endline=$(expr $line_num + $natoms)


#get the name of the job
jobname=$(echo $PWD | awk -F/ '{print $NF}')


#create .xyz file
sed -n ''$startline','$endline'p' OUT.ANI > $jobname.xyz
if [ $? == "0" ]
then
    echo $jobname".xyz" has been created!
else
    echo "Failed to create "$jobname".xyz file"
fi
