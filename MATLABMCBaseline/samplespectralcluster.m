function samplespectralcluster

%文本聚类
%  高质量文本进行聚类
%  聚类的方法采用谱聚类

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% 读写文件目录 %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_sc';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% 每一行代表一条数据
cluster_data = load(read_filename);

[cluster_tag, center, sum_to_center, each_to_center] = spectral_cluster(cluster_data, cluster_number);

% 聚类分析
center_data = zeros(size(cluster_data, 2), cluster_number);
for k = 1 : size(each_to_center, 2)
    [min_value, min_index] = min(each_to_center(:, k));
    center_data(:, k) = cluster_data(min_index, :);
end

% 当前天的聚类数据（聚类中心）写入文件
% 写入后每一列代表一条信息
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center_data, ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag, ' ');

fprintf('\n聚类完毕\n');
time = toc;
fprintf('用时%f秒\n', time);

end

%% 谱聚类
function [cluster_tag, center, sum_to_center, each_to_center] = spectral_cluster(data, cluster_number)

% 计算node之间的相似度矩阵
n = size(data, 1);  % 行数代表数据个数
node_matrix = zeros(n, n);  %顶点度矩阵
degree_matrix = zeros(n, n);  %顶点度矩阵

for i = 1 : n
    for j = i : n
        distance = pdist2(data(i, :), data(j, :), 'Euclidean');
        if distance == 0
            node_matrix(i, j) = 1;
        else
            node_matrix(i, j) = 1 / distance;
        end
        node_matrix(j, i) = node_matrix(i, j);
    end
    degree_matrix(i, i) = sum(node_matrix(i, :));
end

disp('finish the node similarity computing!!!');

% 基于相似度矩阵的NJW谱聚类
% L_matrix = degree_matrix - node_matrix;  % 构建拉普拉斯矩阵
for i = 1 : n
    degree_matrix(i, i) = degree_matrix(i, i) ^ (-1 / 2);
end

L_matrix = degree_matrix * node_matrix * degree_matrix;  % 拉普拉斯矩阵规范化

[E_vectors, E_values] = eigs(L_matrix, cluster_number, 'LM');
k = cluster_number;  % 取特征向量的个数
if k > n
    fpfintf('\n数据个数太少！\n');
else

    % 按行单位化
    for i = 1 : n
        fenmu = norm(E_vectors(i, :));
        for j = 1 : cluster_number
            E_vectors(i, j) = E_vectors(i, j) ./ fenmu;
        end
    end

    % K-Means聚类
    % 注意K-Means聚类输入的数据按行来
    [cluster_tag, center, sum_to_center, each_to_center] = kmeans(E_vectors, cluster_number);
    disp('finish the clustering!!!');
end

end