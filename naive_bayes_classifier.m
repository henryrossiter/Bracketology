stats = csvread('training_data.csv',1,0);
tourney_wins = stats(:, 1);
season_games = stats(:, 3);
season_win_pct = stats(:, 4);
season_ppg = stats(:, 5);
facs = horzcat(season_win_pct,season_games,season_ppg);

Mdl = fitcnb(facs, tourney_wins);

[xx, yy, zz] = meshgrid(.5:.01:1.0,20:.6:50,50:1:100);
succ_pred = predict(Mdl,[xx(:) yy(:) zz(:)]);

sz = size(xx);
succ_pred = reshape(succ_pred,sz);
%postNB = posterior(Mdl,[xx(:) yy(:) zz(:)]);

h = figure;
filename = 'nb_prediction.gif';
for n = 1:.5:55
    az = .5*n+100;
    el = .2*n;
    view(az, el);
    zslice = 50+.4*n;
    xslice = .55+.006*n;
    yslice = [30 40];
    slice([.5:.01:1.0],[20:.6:50],[50:1:100],succ_pred,xslice,yslice,zslice);
    xlabel('win pct')
    ylabel('games played')
    zlabel('ppg')
    cb = colorbar;
    cb.Label.String = 'predicted wins';
    az = n+30;
    el = .7*n+20;
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
