function sampleem

%�ı�����
%  �ı�����
%  ����ķ�������GMM

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_em';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% ÿһ�д���һ������
cluster_data = load(read_filename);
[cluster_tag, model, llh] = emgm(cluster_data', cluster_number);

% �������
center_data = model.mu;

% ��ǰ��ľ������ݣ��������ģ�д���ļ�
% д���ÿһ�д���һ����Ϣ
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center_data, ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag', ' ');

fprintf('\n�������\n');
time = toc;
fprintf('��ʱ%f��\n', time);

end
