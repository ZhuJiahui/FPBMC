function secondcluster

%文本聚类
%  分片合并聚类
%  聚类的方法采用KMeans

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% 读写文件目录 %%
tic;

read_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/merge_cluster_center';
read_directory2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/cluster_tag1';

write_filename1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/cluster_center2.txt';
write_filename2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/cluster_tag2.txt';

% 待聚类的数据总片数
data_files = dir(fullfile(read_directory1, '*.txt'));
cluster_number = 8;

first_cluster_data = load(strcat(read_directory1, '/1.txt'));
data_dimension = size(first_cluster_data, 2);
each_number = size(first_cluster_data, 1);
cluster_data = zeros(length(data_files) * each_number, data_dimension);

for i = 1 : length(data_files)

    % 每一行代表一条数据
    first = 1 + each_number * (i - 1);
    last = each_number * i;
    
    cluster_data(first : last, :) = load(strcat(strcat(read_directory1, '/'), strcat(num2str(i), '.txt')));

end

[cluster_tag, center, sum_to_center, each_to_center] = kmeans(cluster_data, cluster_number, 'emptyaction','singleton');

% 聚类分析
center_data = zeros(size(cluster_data, 2), cluster_number);
for k = 1 : size(each_to_center, 2)
    [min_value, min_index] = min(each_to_center(:, k));
    center_data(:, k) = cluster_data(min_index, :);
end

for i = 1 : length(data_files)
    pre_cluster_tag = load(strcat(strcat(read_directory2, '/'), strcat(num2str(i), '.txt')));

    for j = 1 : size(pre_cluster_tag, 1)
        for k = 1 : cluster_number
            if pre_cluster_tag(j, 1) == k
                pre_cluster_tag(j, 1) = cluster_tag(cluster_number * (i - 1) + k);
            end
        end
    end
    
    dlmwrite(write_filename2, pre_cluster_tag, '-append', 'delimiter', ' ');
end

% 当前天的聚类数据（聚类中心）写入文件
% 写入后每一列代表一条信息
dlmwrite(write_filename1, center_data, ' ');

fprintf('\n聚类完毕\n');
time = toc;
fprintf('用时%f秒\n', time);

end