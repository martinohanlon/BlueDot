package com.stuffaboutcode.bluedot;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

import java.util.ArrayList;
import java.util.HashMap;

class DynamicMatrix extends View {

    private ArrayList<ArrayList<MatrixCell>> mCells;
    private int mCols, mRows;
    private Paint mTextPaint, mCellPaint, mBorderPaint, mLinePaint;
    private float mTextHeight;
    private int mWidth, mHeight;
    int mMatrixWidth, mMatrixHeight;
    int mCellSize;
    private Context mContext;
    private RectF mMatrixBounds = new RectF();

    private HashMap<Integer, MatrixPointer> pointers = new HashMap<Integer, MatrixPointer>();

    public interface DynamicMatrixListener {
        public void onPress(MatrixCell cell, int pointerId, float actual_x, float actual_y);
        public void onMove(MatrixCell cell, int pointerId, float actual_x, float actual_y);
        public void onRelease(MatrixCell cell, int pointerId, float actual_x, float actual_y);
    }

    private DynamicMatrixListener listener;

    public DynamicMatrix(Context context, AttributeSet attrs) {
        super(context, attrs);

        listener = null;
        mContext = context;

        TypedArray a = context.getTheme().obtainStyledAttributes(
                attrs,
                R.styleable.DynamicMatrix,
                0, 0);

        try {
            mCols = a.getInteger(R.styleable.DynamicMatrix_cols, 0);
            mRows = a.getInteger(R.styleable.DynamicMatrix_rows, 0);
        } finally {
            a.recycle();
        }

        init();
    }

    public void setOnUseListener(DynamicMatrixListener listener) {
        this.listener = listener;
    }

    // initialise the matrix
    private void init() {

        mCellPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        mCellPaint.setStyle(Paint.Style.FILL);

        mBorderPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        mBorderPaint.setStyle(Paint.Style.STROKE);
        mBorderPaint.setStrokeWidth(5);
        mBorderPaint.setColor(mContext.getResources().getColor(R.color.darkgrey));

        setupMatrix();
    }

    // when the size changes, re-create the matrix
    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        int xpad = (getPaddingLeft() + getPaddingRight());
        int ypad = (getPaddingTop() + getPaddingBottom());

        mWidth = w - xpad;
        mHeight = h - ypad;

        sizeMatrix();
    }

    // setup matrix is called on init or when the number of rows or cols changes
    // and creates a default matrix with a zero size, its not sized until onSizeChanged
    // is called
    private void setupMatrix() {

        mMatrixWidth = 0;
        mMatrixHeight = 0;
        mCellSize = 0;
        mMatrixBounds = new RectF(0 ,0,0,0);
        // create the cells
        mCells = new ArrayList<ArrayList<MatrixCell>>();
        int color = mContext.getResources().getColor(R.color.defaultCellColor);

        for(int c = 0; c < getCols(); c++) {
            mCells.add(new ArrayList<MatrixCell>());
            for (int r = 0; r < getRows(); r++) {
                mCells.get(c).add(new MatrixCell(
                        c,
                        r,
                        new RectF(0,0,0,0),
                        true,
                        false,
                        color,
                        false));
            }
        }
    }

    // called when the screen size of the matrix needs to change
    private void sizeMatrix() {

        // calc potential size of matrix
        int left = 0, top = 0;
        float borderWidth;

        // find out how big each cell can be
        if ((mWidth / getCols()) < (mHeight / getRows())) {
            borderWidth = (mWidth * Constants.BORDER_THICKNESS);
            mCellSize = (int)((mWidth - borderWidth) / getCols());
            mMatrixWidth = mWidth;
            mMatrixHeight = getRows() * mCellSize;
            top = (mHeight - mMatrixHeight) / 2;
            left = (int)(borderWidth / 2);
        } else {
            borderWidth = (mHeight * Constants.BORDER_THICKNESS);
            mCellSize = (int)((mHeight - borderWidth) / getRows());
            mMatrixWidth = getCols() * mCellSize;
            mMatrixHeight = mHeight;
            top = (int)(borderWidth / 2);
            left = (mWidth - mMatrixWidth) / 2;
        }

        // set the bounds for the matrix
        mMatrixBounds = new RectF(
                left,
                top,
                left + mMatrixWidth,
                top + mMatrixHeight);

        // set the bound for the cells
        for(int c = 0; c < getCols(); c++) {
            for (int r = 0; r < getRows(); r++) {
                mCells.get(c).get(r).setBounds(sizeCell(c, r));
            }
        }

        // set line thickness
        mBorderPaint.setStrokeWidth((float)Math.max(1, mCellSize * Constants.BORDER_THICKNESS));

    }


    private RectF sizeCell(int c, int r) {
        return new RectF(
                (int) mMatrixBounds.left + (c * mCellSize),
                (int) mMatrixBounds.top + (r * mCellSize),
                (int) mMatrixBounds.left + (c * mCellSize) + mCellSize,
                (int) mMatrixBounds.top + (r * mCellSize) + mCellSize);
    }

    // called when the control needs to be drawn
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        // draw matrix
        for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row ) {
                if (cell.getVisible()) mCellPaint.setColor(cell.getColor());
                else mCellPaint.setColor(Color.TRANSPARENT);
                if (cell.getBorder()) {
                    if (cell.getSquare()) {
                        canvas.drawRect(cell.getInnerBounds(), mCellPaint);
                        canvas.drawRect(cell.getBounds(), mBorderPaint);
                    } else {
                        canvas.drawOval(cell.getInnerBounds(), mCellPaint);
                        canvas.drawOval(cell.getBounds(), mBorderPaint);
                    }
                } else {
                    if (cell.getSquare()) {
                        canvas.drawRect(cell.getBounds(), mCellPaint);
                    } else {
                        canvas.drawOval(cell.getBounds(), mCellPaint);
                    }
                }
            }
        }

        // fancy animation stuff, but its a bit weird
        /*for (Integer pointerId : pointers.keySet()){
            MatrixPointer pointer = pointers.get(pointerId);

            float x = pointer.getX();
            float y = pointer.getY();
            RectF cellBounds = pointer.getPressedCell().getBounds();
            float highlightWidth = cellBounds.width() * 0.1f;

            //draw a line from the centre of the cell to the position
            mLinePaint.setColor(pointer.getPressedCell().getMovedColor());
            canvas.drawLine(cellBounds.centerX(), cellBounds.centerY(), x, y, mLinePaint);

            // is pointer inside the pressed cell?
            //if (cellBounds.contains(x,y)){
            //    RectF selectedRect = new RectF(x - highlightWidth, y - highlightWidth, x + highlightWidth, y + highlightWidth);
            //    mCellPaint.setColor(pointer.getPressedCell().getMovedColor());
            //    canvas.drawRect(selectedRect, mCellPaint);
            //}

        }*/
    }

    // manage the touch events
    @Override
    public boolean onTouchEvent(MotionEvent event) {

        int pointerIndex, pointerId;
        MatrixPointer pointer;
        MatrixCell cell;
        float x, y;

        switch(event.getActionMasked()) {

            case MotionEvent.ACTION_DOWN:
                // do the perform click
                performClick();

            case MotionEvent.ACTION_POINTER_DOWN:

                // TODO have a look at the acceleration bit
                pointerIndex = event.getActionIndex();
                x = event.getX(pointerIndex);
                y = event.getY(pointerIndex);

                // was it inside the matrix?
                if (mMatrixBounds.contains(x, y)) {
                    cell = findCellFromXY(x, y);
                    if (cell != null) {
                        // if this cell isnt already pressed, press it
                        if (!cell.getPressed()) {
                            pointerId = event.getPointerId(pointerIndex);
                            pointers.put(pointerId, new MatrixPointer(pointerId, x, y, cell));

                            cell.press();
                            if (listener != null)
                                listener.onPress(cell, pointerId, x, y);
                        }
                    }
                }
                break;

            case MotionEvent.ACTION_UP:

            case MotionEvent.ACTION_POINTER_UP:
                pointerIndex = event.getActionIndex();
                x = event.getX(pointerIndex);
                y = event.getY(pointerIndex);
                pointerId = event.getPointerId(pointerIndex);
                pointer = pointers.get(pointerId);
                if (pointer != null) {
                    cell = pointer.getPressedCell();
                    cell.release();
                    pointers.remove(pointerId);
                    if (listener != null)
                        listener.onRelease(cell, pointerId, x, y);
                }
                break;

            case MotionEvent.ACTION_MOVE:
                int numPointers = event.getPointerCount();

                for (pointerIndex = 0; pointerIndex < numPointers; pointerIndex++) {
                    //pointerIndex = event.getActionIndex();
                    x = event.getX(pointerIndex);
                    y = event.getY(pointerIndex);

                    // was it inside the matrix?
                    if (mMatrixBounds.contains(x, y)) {
                        // was it inside the pressed cell?
                        pointerId = event.getPointerId(pointerIndex);
                        pointer = pointers.get(pointerId);
                        if (pointer != null) {
                            // has this pointer moved?
                            if (pointer.getX() != x && pointer.getY() != y) {
                                pointer.move(x, y);
                                // removed - no need to update the cell view when it is moved
                                // pointer.getPressedCell().moved();
                                if (listener != null)
                                    listener.onMove(pointer.getPressedCell(), pointerId, x, y);
                            }
                        }
                    }
                }
                break;

        }
        return true;
    }

    // finds the cell on the matrix from the xy
    private MatrixCell findCellFromXY(float x, float y) {
        /*for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row) {
                if (cell.getBounds().contains(x, y)) {
                    return cell
                }
            }
        }*/
        int col = (int)(x - mMatrixBounds.left) / mCellSize;
        int row = (int)(y - mMatrixBounds.top) / mCellSize;
        if (col < mCols && row < mRows) {
            return mCells.get(col).get(row);
        } else {
            return null;
        }

    }

    @Override
    public boolean performClick() {
        super.performClick();
        return true;
    }

    // updates the matrix, must be called after each update to the matrix to display the changes
    public void update() {
        invalidate();
        requestLayout();
    }

    // getters and setters
    public ArrayList<ArrayList<MatrixCell>> getCells() {
        return mCells;
    }

    public MatrixCell getCell(int col, int row) {
        return mCells.get(col).get(row);
    }

    public void setSize(int cols, int rows) {
        cols = Math.max(1, cols);
        rows = Math.max(1, rows);
        mCols = cols;
        mRows = rows;
        setupMatrix();
        sizeMatrix();

    }

    public void setColor(int color) {
        for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row ) {
                cell.setColor(color);
            }
        }
    }

    public void setVisible(boolean value) {
        for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row ) {
                cell.setVisible(value);
            }
        }
    }

    public void setBorder(boolean value) {
        for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row ) {
                cell.setBorder(value);
            }
        }
    }

    public void setSquare(boolean value) {
        for (ArrayList<MatrixCell> row : mCells) {
            for (MatrixCell cell : row ) {
                cell.setSquare(value);
            }
        }
    }

    public int getCols() {
        return mCols;
    }

    public void setCols(int value) {
        setSize(value, getRows());
    }

    public int getRows() {
        return mRows;
    }

    public void setRows(int value) {
        setSize(getCols(), value);
    }

    // internal classes

    // keeps track of a single pointer on the matrix
    private class MatrixPointer {

        private int mPointedId;
        private float mX, mY;
        private MatrixCell mPressedCell;

        private MatrixPointer(int pointerId, float x, float y, MatrixCell pressedCell) {
            mPointedId = pointerId;
            mX = x;
            mY = y;
            mPressedCell = pressedCell;
        }
        private void move(float x, float y) {
            mX = x;
            mY = y;
        }
        private MatrixCell getPressedCell() {
            return mPressedCell;
        }
        private float getX() {
            return mX;
        }
        private float getY() {
            return mY;
        }
    }

    // represents a cell on the matrix, used to keep track of the state
    public class MatrixCell {

        private int mRow, mCol, mCurrentColor, mReleasedColor, mPressedColor, mMovedColor;
        private RectF mBounds;
        private boolean mBorder, mPressed, mVisible, mSquare;

        private MatrixCell(int col, int row, RectF bounds, boolean visible, boolean border, int color, boolean square) {
            mCol = col;
            mRow = row;
            mBounds = bounds;
            mBorder = border;
            mPressed = false;
            mVisible = visible;
            mSquare = square;
            updateColors(color);
        }
        /*public int getRow() { return mRow; }
        public int getCol() { return mCol; }*/
        public RectF getBounds() {
            return mBounds;
        }
        private void setBounds(RectF value) {
            mBounds = value;
        }
        public RectF getInnerBounds() {
            float border = (mCellSize * Constants.BORDER_THICKNESS) / 2;
            return new RectF(
                    mBounds.left + border,
                    mBounds.top + border,
                    mBounds.right - border,
                    mBounds.bottom - border);
        }
        public int getColor() {
            return mCurrentColor;
        }
        public int getMovedColor() {
            return mMovedColor;
        }
        public void setColor(int value) {
            updateColors(value);
        }
        public boolean getBorder() {
            return mBorder;
        }
        public void setBorder(boolean value) {
            mBorder = value;
        }
        public boolean getVisible() {
            return mVisible;
        }
        public void setVisible(boolean value) {
            mVisible = value;
        }
        public boolean getSquare() {
            return mSquare;
        }
        public void setSquare(boolean value) {
            mSquare = value;
        }
        public int getCol() {
            return mCol;
        }
        public int getRow() {
            return mRow;
        }
        public float getWidth() {
            return mBounds.right - mBounds.left;
        }
        public float getHeight() {
            return mBounds.bottom - mBounds.top;
        }
        public boolean getPressed() {
            return mPressed;
        }

        // called when the cell is pressed
        private void press() {
            mCurrentColor = mPressedColor;
            mPressed = true;
            invalidate();
            requestLayout();
        }

        // called when the cell is released
        private void release() {
            mCurrentColor = mReleasedColor;
            mPressed = false;
            invalidate();
            requestLayout();
        }

        // called when the cell is moved
        private void moved() {
            invalidate();
            requestLayout();
        }

        // manages the colors in the cell
        private void updateColors(int color) {
            mReleasedColor = color;
            mPressedColor = manipulateColor(color, 0.85f);
            mMovedColor = manipulateColor(color, 0.7f);

            if (mPressed) {
                mCurrentColor = mPressedColor;
            } else {
                mCurrentColor = mReleasedColor;
            }
        }

        // manipulates a color
        private int manipulateColor(int color, float factor) {
            int a = Color.alpha(color);
            int r = Math.round(Color.red(color) * factor);
            int g = Math.round(Color.green(color) * factor);
            int b = Math.round(Color.blue(color) * factor);
            return Color.argb(a,
                    Math.min(r,255),
                    Math.min(g,255),
                    Math.min(b,255));
        }
    }
}

