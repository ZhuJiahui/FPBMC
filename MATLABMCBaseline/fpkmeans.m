function fpkmeans
%文本聚类
%  高质量文本的频繁项集进行聚类
%  聚类的方法采用K-Means

%  B506
%  Computer Science School
%  Wuhan University, Wuhan 430072 China
%  Huang Jimin
%  2014-3-28

%%%%% Baseline1 Step 2

%读取数据
data=load('vsm1.txt');
%聚类数目
cluster_number=9;
n=size(data,1);
%kmeans聚类
[labels, center, sumD, D] = kmeans(data, cluster_number);
%计算向量与对应聚类中心的平均距离
cen_num = zeros(cluster_number,1);
for i = 1 : n
    cen_num(labels(i)) = cen_num(labels(i))+1;
end
for i = 1 : cluster_number
    sumD(i) = sumD(i) / cen_num(i);
end
sums= sum(sumD) / cluster_number;
%计算与聚类中心最接近的向量
mins = zeros(cluster_number,1);
for i = 1 : cluster_number
    temp=min(D(:,i));
    mins(i)=find(D(:,i)==temp,1);
end
%计算聚类中心之间的平均距离
distance=zeros(cluster_number,cluster_number);
for i= 1 : cluster_number
    for j= i: cluster_number
        distance(i,j)=pdist2(center(i,:), center(j, :), 'Euclidean');
    end
end
distances=sum(sum(distance)) / (cluster_number *(cluster_number-1) / 2);
%计算比值
force=sums/distances;
%输出文件
dlmwrite('k-result-centroids.txt', mins,' ');
dlmwrite('k-result-labels.txt', labels,' ');  % 最后只需该文件
dlmwrite('k-result-c.txt', sums,' ');
dlmwrite('k-result-s.txt', distances,' ');
dlmwrite('k-result-cs.txt', force,' ');
end