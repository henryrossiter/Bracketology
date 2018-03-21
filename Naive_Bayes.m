M = csvread('training_data.csv',1,1);
stats = M(:, [3 4]);
seed_diff = stats(:, 1);
exp_diff = stats(:, 2);
outcomes = M(:, 6);
types = categorical(outcomes);
labels = categories(types);

gscatter(seed_diff, exp_diff, outcomes,'rgb','osd');
xlabel('difference in seed');
ylabel('difference in experience');
N = size(M,1);

mdlNB = fitcnb(stats,types);

[xx1, xx2] = meshgrid(-15:.1:15,-1:.01:1);
[ypred, postNB] = predict(mdlNB,[xx1(:) xx2(:)]);

sz = size(xx1);
figure(1),
surf(xx1,xx2,reshape(postNB(:,2),sz),'EdgeColor','none'), hold on
%surf(xx1,xx2,reshape(postNB(:,1),sz),'EdgeColor','none')
xlabel('difference in seed');
ylabel('difference in experience'); 
h = colorbar;
set(get(h,'label'),'string','Probability of Winning');
set(gcf,'renderer','painters')
view(2)