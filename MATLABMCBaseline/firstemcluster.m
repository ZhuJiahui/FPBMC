function firstemcluster

%�ı�����
%  ��Ƭ�����ı�����
%  ����ķ�������GMM

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
tic;

read_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/segment/vsm';

write_directory1 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/cluster_center1';
write_directory2 = 'D:/Local/workspace/MicroblogCluster/dataset/global_em/cluster_tag1';

if ~isdir(write_directory1)
    mkdir(write_directory1);
end
if ~isdir(write_directory2)
    mkdir(write_directory2);
end

% �������������Ƭ��
data_files = dir(fullfile(read_directory1, '*.txt'));
cluster_number = 5;

for i = 1 : length(data_files)
    
    fprintf('���ڴ����%dƬ����\n', i);
    
    % ÿһ�д���һ������
    cluster_data = load(strcat(strcat(read_directory1, '/'), strcat(num2str(i), '.txt')));
    
    [cluster_tag, model, llh] = emgm(cluster_data', cluster_number);
    
    % �������
    center_data = model.mu;
    
    % ��ǰ��ľ������ݣ��������ģ�д���ļ�
    % д���ÿһ�д���һ����Ϣ
    dlmwrite(strcat(strcat(write_directory1, '/'), strcat(num2str(i), '.txt')), center_data, ' ');
    dlmwrite(strcat(strcat(write_directory2, '/'), strcat(num2str(i), '.txt')), cluster_tag', ' ');
    
    fprintf('��%dƬ���ݴ������\n', i);

end

fprintf('\n�������ݾ������\n');
time = toc;
fprintf('��ʱ%f��\n', time);
end
