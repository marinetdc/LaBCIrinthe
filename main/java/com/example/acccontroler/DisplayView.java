package com.example.acccontroler;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Point;
import android.util.AttributeSet;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.util.ArrayList;
import java.util.List;

/**
 * DisplayView is responsible for displaying the arrow to indicate the direction of the gravitational force
 */
public class DisplayView extends SurfaceView implements SurfaceHolder.Callback
{
    /* static variables ***********************************************************************************************/

    static final float EARTH_GRAVITY = 9.807f;

    /* Member variables ***********************************************************************************************/

    private SurfaceHolder holder;
    private Paint arrowPaint;
    private float scaleX = 0.0f;
    private float scaleY = 0.0f;

    private List<Point> arrow = new ArrayList<>();

    private int squareSize = 100;

    /* Constructors ***************************************************************************************************/

    public DisplayView(Context context)
    {
        super(context);
        init();
    }

    public DisplayView(Context context, AttributeSet attributeSet)
    {
        super(context, attributeSet);
        init();
    }

    /* Public methods *************************************************************************************************/

    @Override
    public void surfaceCreated(SurfaceHolder surfaceHolder)
    {
        arrowPaint = new Paint();
        arrowPaint.setColor(Color.RED);
        arrowPaint.setStrokeWidth(1);
        arrowPaint.setStyle(Paint.Style.FILL);
        drawOnThread();
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) { }

    @Override
    public void surfaceDestroyed(SurfaceHolder surfaceHolder) { }

    /**
     * Redraw the arrow
     * @param x x
     * @param y y
     */
    public void update(float x, float y)
    {

        // Gravity vector is defined as opposite of what you’d expect, so operand - is needed
        scaleX = -x / EARTH_GRAVITY;
        scaleY = -y / EARTH_GRAVITY;
        drawOnThread();
    }

    /* Private methods ************************************************************************************************/

    /**
     * Initialize
     */
    private void init()
    {
        holder = getHolder();
        holder.addCallback(this);
        makeArrow();
    }

    /**
     * Apply appropriate affine transformations and draw
     * @param canvas canvas to draw on
     */
    private void drawArrow(Canvas canvas)
    {
        canvas.drawColor(Color.WHITE);

        int centerX, centerY;
        centerX = getWidth() / 2;
        centerY = getHeight() / 2;

        Path arrowPath = new Path();

        // Maximum length is half of the width of the screen
        List<Point> arrowPoints = lengthen(arrow, getLength() * getWidth() / 2 / squareSize);

        // Rotate back (anticlockwise) by pi/2 because the original arrow is vertical
        arrowPoints = rotate(arrowPoints, (float) (getAngle() - Math.PI / 2));

        // Center the arrow
        arrowPoints = translate(arrowPoints, centerX, centerY);

        // Draw the arrow
        arrowPath.moveTo(arrowPoints.get(0).x, arrowPoints.get(0).y);
        for (int i = 1; i < arrowPoints.size(); i++)
        {
            arrowPath.lineTo(arrowPoints.get(i).x , arrowPoints.get(i).y);
        }
        arrowPath.close();

        arrowPaint.setColor(getColor(getLength()));

        canvas.drawPath(arrowPath, arrowPaint);
    }

    /**
     * Draw on a new thread
     */
    private void drawOnThread()
    {
        Thread t = new Thread(new Runnable()
        {
            @Override
            public void run()
            {
                Canvas canvas = null;
                try
                {
                    canvas = holder.lockCanvas(null);
                    if (canvas != null)
                        drawArrow(canvas);

                } finally
                {
                    if (canvas != null)
                        holder.unlockCanvasAndPost(canvas);
                }
            }
        });

        t.start();
    }

    /**
     * Make an arrow shape and store in a list
     */
    private void makeArrow()
    {
        // An arrow that starts at the middle of the bottom side of a square and extends
        // up to the top end

        int bodyHalfWidth = 5;
        int headHeight = 10;
        int headHalfWidth = 20;

        // Right vertical line going up
        arrow.add(new Point(squareSize / 2 + bodyHalfWidth, squareSize));
        arrow.add(new Point(squareSize / 2 + bodyHalfWidth, headHeight));

        // Arrow head
        arrow.add(new Point(squareSize / 2 + headHalfWidth, headHeight));
        arrow.add(new Point(squareSize / 2, 0));
        arrow.add(new Point(squareSize / 2 - headHalfWidth, headHeight));

        // Left vertical line going down
        arrow.add(new Point(squareSize / 2 - bodyHalfWidth, headHeight));
        arrow.add(new Point(squareSize / 2 - bodyHalfWidth, squareSize));

        // Center at (0, 0)
        arrow = translate(arrow,-squareSize / 2, -squareSize);
    }

    /**
     * Translate the arrow
     * @param points list of points
     * @param x x
     * @param y y
     * @return translated points
     */
    private List<Point> translate(List<Point> points, int x, int y)
    {
        List<Point> result = new ArrayList<>();

        for (Point point : points)
        {
            int outX = point.x + x;
            int outY = point.y + y;

            result.add(new Point(outX, outY));
        }

        return result;
    }

    /**
     * Enlarge along y-axis
     * @param points list of points
     * @param ratio ratio by which to lengthen
     * @return resulting points
     */
    private List<Point> lengthen(List<Point> points, float ratio)
    {
        List<Point> result = new ArrayList<>();

        for (Point point : points)
        {
            int y = (int) (point.y * ratio);

            result.add(new Point(point.x, y));
        }

        return result;
    }

    /**
     * Rotate list of points
     * @param points list of points
     * @param angle angle in radian
     * @return rotated points
     */
    private List<Point> rotate(List<Point> points, float angle)
    {
        List<Point> result = new ArrayList<>();

        for (Point point : points)
        {
            int x = (int) (Math.sin(angle) * point.y + Math.cos(angle) * point.x);
            int y = (int) (Math.cos(angle) * point.y - Math.sin(angle) * point.x);

            result.add(new Point(x, y));
        }

        return result;
    }

    /**
     * Get Euclidean length
     * @return length
     */
    private float getLength()
    {
        return (float) Math.sqrt((double) (scaleX * scaleX + scaleY * scaleY));
    }

    /**
     * Get angle from x and y coordinates
     * @return angle in radian
     */
    private float getAngle()
    {
        // Angle in device coordinate, i.e. x: right is positive, y: up is positive
        return (float) Math.atan2(scaleY, scaleX);
    }

    /**
     * Get color from a gradient of of blue and red. Blue if value is 0 red if 1
     * @param length Length of the arrow from which color is calculated
     * @return color in int
     */
    private int getColor(float length)
    {
        // Length is between 0 and 1
        int blue = (int) ((1 - length) * 255);
        int red  = (int) (length * 255);

        return Color.rgb(red, 0, blue);
    }
}

