function samplespectralcluster

%�ı�����
%  �������ı����о���
%  ����ķ��������׾���

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  zhujiahui@whu.edu.cn
%  2014-3-28

%% ��д�ļ�Ŀ¼ %%
tic;

read_filename = 'D:/Local/workspace/MicroblogCluster/dataset/high_quality_data/sample_vsm.txt';

write_directory = 'D:/Local/workspace/MicroblogCluster/dataset/sample_sc';

if ~isdir(write_directory)
    mkdir(write_directory);
end

cluster_number = 8;

% ÿһ�д���һ������
cluster_data = load(read_filename);

[cluster_tag, center, sum_to_center, each_to_center] = spectral_cluster(cluster_data, cluster_number);

% �������
center_data = zeros(size(cluster_data, 2), cluster_number);
for k = 1 : size(each_to_center, 2)
    [min_value, min_index] = min(each_to_center(:, k));
    center_data(:, k) = cluster_data(min_index, :);
end

% ��ǰ��ľ������ݣ��������ģ�д���ļ�
% д���ÿһ�д���һ����Ϣ
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_center.txt'), center_data, ' ');
dlmwrite(strcat(strcat(write_directory, '/'), 'cluster_tag.txt'), cluster_tag, ' ');

fprintf('\n�������\n');
time = toc;
fprintf('��ʱ%f��\n', time);

end

%% �׾���
function [cluster_tag, center, sum_to_center, each_to_center] = spectral_cluster(data, cluster_number)

% ����node֮������ƶȾ���
n = size(data, 1);  % �����������ݸ���
node_matrix = zeros(n, n);  %����Ⱦ���
degree_matrix = zeros(n, n);  %����Ⱦ���

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

% �������ƶȾ����NJW�׾���
% L_matrix = degree_matrix - node_matrix;  % ����������˹����
for i = 1 : n
    degree_matrix(i, i) = degree_matrix(i, i) ^ (-1 / 2);
end

L_matrix = degree_matrix * node_matrix * degree_matrix;  % ������˹����淶��

[E_vectors, E_values] = eigs(L_matrix, cluster_number, 'LM');
k = cluster_number;  % ȡ���������ĸ���
if k > n
    fpfintf('\n���ݸ���̫�٣�\n');
else

    % ���е�λ��
    for i = 1 : n
        fenmu = norm(E_vectors(i, :));
        for j = 1 : cluster_number
            E_vectors(i, j) = E_vectors(i, j) ./ fenmu;
        end
    end

    % K-Means����
    % ע��K-Means������������ݰ�����
    [cluster_tag, center, sum_to_center, each_to_center] = kmeans(E_vectors, cluster_number);
    disp('finish the clustering!!!');
end

end