num_episodes=1000
max_pedestrians=25
max_vehicles=25
length_episode=1000

destination=$1
port=$2

for i in `seq $num_episodes`;
do
  num_pedestrians=$((1 + $RANDOM % $max_pedestrians));
  num_vehicles=$((1 + $RANDOM % $max_vehicles));
  python oatomobile/examples/generate-dataset.py -w ${num_pedestrians} -v ${num_vehicles} -s ${length_episode} -d ${destination} -p ${port};
done
