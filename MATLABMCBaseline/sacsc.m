function sacsc
%�ı�����
%  �������ı���Ƶ������о���
%  ����ķ�������SAC_SC

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  Huang Jimin
%  2014-3-28

%%%%% Step 11

%�������ƾ����ļ�
data = load('similarity_matrix1.txt');
cluster_number = 9;
n = size(data,1);
degree_matrix = zeros(n, n);
%����Ⱦ���
for i = 1 : n
    degree_matrix(i, i) = sum(data(i, :));
end

%���� �ǹ淶�� ������˹����
L_matrix = degree_matrix - data;
for i = 1 : n
    degree_matrix(i, i) = degree_matrix(i, i) ^ (-1 / 2);
end

%������˹����淶��
L_matrix = degree_matrix * L_matrix * degree_matrix;

%����������˹��������ֵ����������
[e_vectors,e_values] = eig(L_matrix);
%ѡȡǰk����������ֵ
select_E_vectors = e_vectors(:, 1 : cluster_number);
norm_select_E_vectors = zeros(n, cluster_number);

for i = 1 : n
    for j = 1 : cluster_number
        norm_select_E_vectors(i, j) = select_E_vectors(i, j) / (sum(select_E_vectors(i, :) .^ 2) ^ (0.5));
    end
end

%kmeans����
[labels, center, sumD, D] = kmeans(norm_select_E_vectors, cluster_number, 'emptyaction','singleton');
%�����������Ӧ�������ĵ�ƽ������
cen_num = zeros(cluster_number,1);
for i = 1 : n
    cen_num(labels(i)) = cen_num(labels(i))+1;
end
for i = 1 : cluster_number
    sumD(i) = sumD(i) / cen_num(i);
end
sums= sum(sumD) / cluster_number;
%���������������ӽ�������
mins = zeros(cluster_number,1);
for i = 1 : cluster_number
    temp=min(D(:,i));
    mins(i)=find(D(:,i)==temp);
end

%�����������֮���ƽ������
distance=zeros(cluster_number,cluster_number);
for i= 1 : cluster_number
    for j= i: cluster_number
        distance(i,j)=pdist2(center(i,:), center(j, :), 'Euclidean');
    end
end
distances=sum(sum(distance)) / (cluster_number *(cluster_number-1) / 2);
%�����ֵ
force=sums/distances;
%����ļ�
dlmwrite('sc-result-centroids.txt', mins);
dlmwrite('sc-result-labels.txt', labels);  % ���ֻ����ļ�
dlmwrite('sc-result-c.txt', sums);
dlmwrite('sc-result-s.txt', distances);
dlmwrite('sc-result-cs.txt', force);
end