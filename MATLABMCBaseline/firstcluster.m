function firstcluster

%�ı�����
%  ��Ƭ�����ı�����
%  ����ķ�������KMeans

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
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

% �������������Ƭ��
data_files = dir(fullfile(read_directory1, '*.txt'));
file_number = 1;
cluster_number = 8;

for i = 1 : length(data_files)
    
    fprintf('���ڴ����%dƬ����\n', i);
    
    % ÿһ�д���һ������
    cluster_data = load(strcat(strcat(read_directory1, '/'), strcat(num2str(i), '.txt')));
    
    [cluster_tag, center, sum_to_center, each_to_center] = kmeans(cluster_data, cluster_number, 'emptyaction','singleton');
    
    % �������
    center_data = zeros(size(cluster_data, 2), cluster_number);
    for k = 1 : size(each_to_center, 2)
        [min_value, min_index] = min(each_to_center(:, k));
        center_data(:, k) = cluster_data(min_index, :);
    end
    
    % ��ǰ��ľ������ݣ��������ģ�д���ļ�
    % д���ÿһ�д���һ����Ϣ
    dlmwrite(strcat(strcat(write_directory1, '/'), strcat(num2str(file_number), '.txt')), center_data, ' ');
    dlmwrite(strcat(strcat(write_directory2, '/'), strcat(num2str(file_number), '.txt')), cluster_tag, ' ');
    file_number = file_number + 1;
    
    fprintf('��%dƬ���ݴ������\n', i);

end

fprintf('\n�������ݾ������\n');
time = toc;
fprintf('��ʱ%f��\n', time);

end