function samplekmeans

%文本聚类
%  高质量文本进行聚类
%  聚类的方法采用KMeans

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% 读写文件目录 %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_kmeans';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% 每一行代表一条数据
cluster_data = load(read_filename);

[cluster_tag, center, sum_to_center, each_to_center] = kmeans(cluster_data, cluster_number, 'emptyaction','singleton');

% 聚类分析
center_data = zeros(size(cluster_data, 2), cluster_number);
for k = 1 : size(each_to_center, 2)
    [min_value, min_index] = min(each_to_center(:, k));
    center_data(:, k) = cluster_data(min_index, :);
end

% 当前天的聚类数据（聚类中心）写入文件
% 写入后每一列代表一条信息
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center', ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag, ' ');

fprintf('\n聚类完毕\n');
time = toc;
fprintf('用时%f秒\n', time);

end