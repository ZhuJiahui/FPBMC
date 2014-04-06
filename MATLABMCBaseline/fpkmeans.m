function fpkmeans
%�ı�����
%  �������ı���Ƶ������о���
%  ����ķ�������K-Means

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  Huang Jimin
%  2014-3-28

%%%%% Baseline1 Step 2

%��ȡ����
data=load('vsm1.txt');
%������Ŀ
cluster_number=9;
n=size(data,1);
%kmeans����
[labels, center, sumD, D] = kmeans(data, cluster_number);
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
    mins(i)=find(D(:,i)==temp,1);
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
dlmwrite('k-result-centroids.txt', mins,' ');
dlmwrite('k-result-labels.txt', labels,' ');  % ���ֻ����ļ�
dlmwrite('k-result-c.txt', sums,' ');
dlmwrite('k-result-s.txt', distances,' ');
dlmwrite('k-result-cs.txt', force,' ');
end