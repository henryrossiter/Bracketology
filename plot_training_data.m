stats = csvread('training_data.csv',1,0);
tourney_wins = stats(:, 1);
season_games = stats(:, 3);
season_win_pct = stats(:, 4);
season_ppg = stats(:, 5);

%plot data to model
h = figure;
scatter3(season_win_pct,season_games,season_ppg,2.*tourney_wins.^2+5,tourney_wins,'filled')  ;  % draw the scatter plot
ax = gca;
xlabel('win pct')
xlim([.5 1.0])
ylabel('games played')
ylim([20 40])
zlabel('ppg')
zlim([50 100])

cb = colorbar;                                     % create and label the colorbar
cb.Label.String = 'wins';

filename = 'lin_reg.gif';
for n = 1:.5:80
    az = n;
    el = .6*n;
    view(az, el);
    drawnow
      % Capture the plot as an image
      frame = getframe(h);
      im = frame2im(frame);
      [imind,cm] = rgb2ind(im,256);
      % Write to the GIF File
      if n == 1
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf,'DelayTime',.1);
      else
          imwrite(imind,cm,filename,'gif','WriteMode','append','DelayTime',.1);
      end
end