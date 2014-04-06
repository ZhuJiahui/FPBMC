function samplekmeans

%�ı�����
%  �������ı����о���
%  ����ķ�������KMeans

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_kmeans';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% ÿһ�д���һ������
cluster_data = load(read_filename);

[cluster_tag, center, sum_to_center, each_to_center] = kmeans(cluster_data, cluster_number, 'emptyaction','singleton');

% �������
center_data = zeros(size(cluster_data, 2), cluster_number);
for k = 1 : size(each_to_center, 2)
    [min_value, min_index] = min(each_to_center(:, k));
    center_data(:, k) = cluster_data(min_index, :);
end

% ��ǰ��ľ������ݣ��������ģ�д���ļ�
% д���ÿһ�д���һ����Ϣ
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center', ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag, ' ');

fprintf('\n�������\n');
time = toc;
fprintf('��ʱ%f��\n', time);

end