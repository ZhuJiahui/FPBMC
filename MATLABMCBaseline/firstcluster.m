function firstcluster

%文本聚类
%  分片进行文本聚类
%  聚类的方法采用KMeans

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% 读写文件目录 %%
tic;

read_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/segment/vsm';
% read_directory2 = 'D:/Local/workspace/MicroblogCluster/dataset/segment/weibo_id';

write_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/cluster_center1';
write_directory2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_kmeans/cluster_tag1';

if ~isdir(write_directory1)
    mkdir(write_directory1);
end
if ~isdir(write_directory2)
    mkdir(write_directory2);
end

% 待聚类的数据总片数
data_files = dir(fullfile(read_directory1, '*.txt'));
file_number = 1;
cluster_number = 8;

for i = 1 : length(data_files)
    
    fprintf('正在处理第%d片数据\n', i);
    
    % 每一行代表一条数据
    cluster_data = load(strcat(strcat(read_directory1, '/'), strcat(num2str(i), '.txt')));
    
    [cluster_tag, center, sum_to_center, each_to_center] = kmeans(cluster_data, cluster_number, 'emptyaction','singleton');
    
    % 聚类分析
    center_data = zeros(size(cluster_data, 2), cluster_number);
    for k = 1 : size(each_to_center, 2)
        [min_value, min_index] = min(each_to_center(:, k));
        center_data(:, k) = cluster_data(min_index, :);
    end
    
    % 当前天的聚类数据（聚类中心）写入文件
    % 写入后每一列代表一条信息
    dlmwrite(strcat(strcat(write_directory1, '/'), strcat(num2str(file_number), '.txt')), center_data, ' ');
    dlmwrite(strcat(strcat(write_directory2, '/'), strcat(num2str(file_number), '.txt')), cluster_tag, ' ');
    file_number = file_number + 1;
    
    fprintf('第%d片数据处理完毕\n', i);

end

fprintf('\n所有数据聚类完毕\n');
time = toc;
fprintf('用时%f秒\n', time);

end