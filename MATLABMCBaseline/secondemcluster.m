function secondemcluster

%�ı�����
%  ��Ƭ�ϲ�����
%  ����ķ�������GMM��EM�㷨

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
tic;

read_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/merge_cluster_center';
read_directory2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/cluster_tag1';

write_filename1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/cluster_center2.txt';
write_filename2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/cluster_tag2.txt';

% �������������Ƭ��
data_files = dir(fullfile(read_directory1, '*.txt'));
cluster_number = 8;

first_cluster_data = load(strcat(read_directory1, '/1.txt'));
data_dimension = size(first_cluster_data, 2);
each_number = size(first_cluster_data, 1);
cluster_data = zeros(length(data_files) * each_number, data_dimension);

for i = 1 : length(data_files)

    % ÿһ�д���һ������
    first = 1 + each_number * (i - 1);
    last = each_number * i;
    
    cluster_data(first : last, :) = load(strcat(strcat(read_directory1, '/'), strcat(num2str(i), '.txt')));

end

[cluster_tag, model, llh] = emgm(cluster_data', cluster_number);

% �������

for i = 1 : length(data_files)
    pre_cluster_tag = load(strcat(strcat(read_directory2, '/'), strcat(num2str(i), '.txt')));

    for j = 1 : size(pre_cluster_tag, 1)
        pre_cluster_tag(j, 1) = cluster_tag(pre_cluster_tag(j, 1) + (i - 1) * each_number);
%         
%         for k = 1 : cluster_number
%             if cluster_tag(cluster_number * (i - 1) + k)
%                 
%             end
%             if pre_cluster_tag(j, 1) == k
%                 pre_cluster_tag(j, 1) = cluster_tag(cluster_number * (i - 1) + k);
%             end
%         end
    end
    
    dlmwrite(write_filename2, pre_cluster_tag, '-append', 'delimiter', ' ');
end

% ��ǰ��ľ������ݣ��������ģ�д���ļ�
% д���ÿһ�д���һ����Ϣ
dlmwrite(write_filename1, model.mu, ' ');

fprintf('\n�������\n');
time = toc;
fprintf('��ʱ%f��\n', time);

end