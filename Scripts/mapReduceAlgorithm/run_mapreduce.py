#!/usr/bin/env python3
import subprocess
import os

# hadoop directories
hdfs_input_dir = "/coffee-sales-project/coffee_sales_input"
hdfs_output_dir = "/coffee-sales-project/coffee_sales_output"

# local paths
local_input = "coffee_shop_sales.csv"
local_output_dir = "../../Deprecated/mapreduce_output"

# store in mapreduce_output/daily_revenue_per_store.tsv
local_output_file = os.path.join(local_output_dir, "daily_revenue_per_store.tsv")

# check if local output directory exists
os.makedirs(local_output_dir, exist_ok=True)

# upload input file to hdfs
print("Uploading input file to HDFS...")
subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_input_dir], check=True)
subprocess.run(["hdfs", "dfs", "-put", "-f", local_input, hdfs_input_dir], check=True)

# remove previous hdfs output if exists
print("Removing Deprecated HDFS output if it exists...")
subprocess.run(["hdfs", "dfs", "-rm", "-r", "-f", hdfs_output_dir], check=True)

# hadoop streaming jar location
hadoop_streaming_jar = "/opt/homebrew/Cellar/hadoop/3.4.2/libexec/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"

# run hadoop streaming job
subprocess.run([
    "hadoop", "jar", hadoop_streaming_jar,
    "-input", os.path.join(hdfs_input_dir, "coffee_shop_sales.csv"),
    "-output", hdfs_output_dir,
    "-mapper", "mapper.py",
    "-reducer", "reducer.py",
    "-file", "mapper.py",
    "-file", "reducer.py"
], check=True)

# check hdfs if output files exist
print("Verifying HDFS output files...")
result = subprocess.run(["hdfs", "dfs", "-ls", hdfs_output_dir], capture_output=True, text=True, check=True)
print(result.stdout)

# copy hdfs output into local output directory
subprocess.run([
    "hdfs", "dfs", "-getmerge",
    f"{hdfs_output_dir}/*",
    local_output_file
], check=True)

print(f"MapReduce job complete. Output saved to: {local_output_file}")

# note: the output isn't being sorted by date, due to the un-padded date format.
