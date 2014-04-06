function sampleem

%文本聚类
%  文本聚类
%  聚类的方法采用GMM

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% 读写文件目录 %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_em';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% 每一行代表一条数据
cluster_data = load(read_filename);
[cluster_tag, model, llh] = emgm(cluster_data', cluster_number);

% 聚类分析
center_data = model.mu;

% 当前天的聚类数据（聚类中心）写入文件
% 写入后每一列代表一条信息
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center_data, ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag', ' ');

fprintf('\n聚类完毕\n');
time = toc;
fprintf('用时%f秒\n', time);

end
